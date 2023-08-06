from typing import Union
import signal
import logging
from threading import Thread
from multiprocessing import managers, Manager, Process, Event
from multiprocessing.queues import JoinableQueue
from time import time, sleep
import abc

class WorkUnit():
    def __init__(self, id: str=None, payload=None, type: str="process"):
        self.id = id
        self.payload = payload
        self.type = type
        self.start_ts = time()
        self.finish_ts = None


class PipeStage(Process):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.ticks: managers.Value = None
        self.stopped: Event = None
        self.__main_thread = Thread(target=self.work)

    def join_pipeline(self, ticks: managers.Value, stopped: Event):
        self.ticks = ticks
        self.stopped = stopped

    def tick(self):
        if self.ticks:
            current = self.ticks.get()
            self.ticks.set(current + 1)

    def block_until_stopped(self):
        while not self.stopped.is_set():
            sleep(.5)

    @abc.abstractmethod
    def will_start(self):
        pass

    @abc.abstractmethod
    def will_stop(self):
        pass

    @abc.abstractmethod
    def work(self):
        pass

    @abc.abstractmethod
    def ports(self):
        pass

    def run(self):
        try:
            self.will_start()
            self.__main_thread.start()
            self.block_until_stopped()
            self.will_stop()
        except KeyboardInterrupt:
            self.will_stop()    

class OutputPort():
    def __init__(self, name: str, owner: PipeStage):
        self.name = name
        self.direction = "OUTPUT"
        self.owner = owner
        self.__queue = None

    def connect_to(self, queue: 'PipeQueue'):
        if self.__queue:
            raise Exception("port already connected")
        self.__queue = queue
        queue.track_producer(self)

    def put(self, work: WorkUnit):
        if not self.__queue:
            raise Exception("port not connected")
        self.__queue.put(work)

class InputPort():
    def __init__(self, name: str, owner: PipeStage):
        self.name = name
        self.direction = "INPUT"
        self.owner = owner
        self.queue = None

    def __safe_get_queue(self):
        if not self.queue:
            raise Exception("port not connected")
        return self.queue

    def connect_to(self, queue: 'PipeQueue'):
        if self.queue:
            raise Exception("port already connected")
        self.queue = queue
        queue.track_consumer(self)

    def get(self, block: bool=True, timeout: int=None):
        queue = self.__safe_get_queue()
        return queue.get(block=block, timeout=timeout)

    def get_or_continue(self):
        queue = self.__safe_get_queue()
        if not queue.empty():
            return queue.get_nowait()
        return None

    def yield_until_empty(self):
        queue = self.__safe_get_queue()
        while not queue.empty():
            yield queue.get_nowait()

    def drop_all_but_last(self):
        queue = self.__safe_get_queue()
        while queue.qsize() > 1:
            queue.get_nowait()
            queue.task_done()
        return queue.get()

    def qsize(self):
        queue = self.__safe_get_queue()
        return queue.qsize()

    def task_done(self):
        queue = self.__safe_get_queue()
        queue.task_done()

AnyPort = Union[InputPort, OutputPort]

class PipeQueue(JoinableQueue):
    def __init__(self, name: str, ctx, maxsize: int=None):
        super().__init__(ctx=ctx, maxsize=maxsize)
        self.name = name
        self.producers = []
        self.consumers = []
    
    def track_producer(self, port: OutputPort):
        self.producers.append(port)

    def track_consumer(self, port: InputPort):
        self.consumers.append(port)


class Pipeline():
    def __init__(self):
        self.__ctx = managers.get_context()
        self.__manager = Manager()
        self.__stopped = Event()
        self.stages = {}
        self.queues = {}
        self.start_ts = None
        self.ticks_ts = None

    def add_stage(self, stage: PipeStage):
        ticks = self.__manager.Value('i', 0)
        stage.join_pipeline(ticks, self.__stopped)
        self.stages[stage.name] = stage

    def reset_ticks(self):
        self.ticks_ts = time()
        for _, stage in self.stages.items():
            stage.ticks.set(0)

    def add_pipe(self, name: str, maxsize=10000):
        queue = PipeQueue(name=name, ctx=self.__ctx, maxsize=maxsize)
        self.queues[name] = queue
        return queue

    def start(self):
        self.start_ts = time()
        self.ticks_ts = self.start_ts

        for name, stage in self.stages.items():
            logging.debug(f"starting stage {name}")
            stage.start()

    def stop(self):
        self.__stopped.set()

    def join(self):
        for name, stage in self.stages.items():
            logging.debug(f"joining stage {name}")
            stage.join()

    def terminate(self):
        for name, stage in self.stages.items():
            logging.debug(f"terminating stage {name}")
            stage.terminate()
