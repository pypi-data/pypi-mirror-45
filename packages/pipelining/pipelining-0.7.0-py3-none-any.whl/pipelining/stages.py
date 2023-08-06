from typing import Iterable, Union
from time import time
from .structure import InputPort, OutputPort, PipeStage, WorkUnit

class EmitterStage(PipeStage):
    def __init__(self, name: str, emitter: callable = None):
        super().__init__(name)
        self.__emitter = emitter
        self.output = OutputPort("output", self)

    def ports(self):
        yield self.output

    def emit(self):
        return self.__emitter()

    def work(self):
        for work in self.emit():
            self.output.put(work)
            self.work_done()

class MapperStage(PipeStage):
    def __init__(self, name: str, mapper: callable = None):
        super().__init__(name)
        self.input = InputPort("input", self)
        self.output = OutputPort("output", self)
        self.__mapper = mapper

    def ports(self):
        yield self.input
        yield self.output

    def map(self, unit: WorkUnit)->Iterable[WorkUnit]:
        mapped = self.__mapper(unit)
        
        if not mapped:
            return

        if isinstance(mapped, Iterable):
            for unit in mapped:
                yield unit

        yield mapped

    def work(self):
        while True:
            original = self.input.get()
            for unit in self.map(original):
                self.output.put(unit)
            self.input.task_done()
            self.work_done()


class ForkStage(PipeStage):
    def __init__(self, name: str, output_count: int):
        super().__init__(name)
        self.input = InputPort("input", self)
        self.outputs = []
        
        for i in range(0, output_count):
            port = OutputPort(f"output_{i}", self)
            self.outputs.append(port)

    def ports(self):
        yield self.input
        for output in self.outputs:
            yield output

    def work(self):
        while True:
            work = self.input.get()
            for output in self.outputs:
                output.put(work)
            self.input.task_done()
            self.work_done()


class ThrottleStage(MapperStage):
    def __init__(self, name: str, max_throughput: float):
        super().__init__(name=name)
        self.__min_delay = 1 / max_throughput
        self.__last_ts = None

    def map(self, unit: WorkUnit):
        now = time()
        delta = now - self.__last_ts if self.__last_ts else None

        if not delta or delta > self.__min_delay:
            self.__last_ts = now
            yield unit

class BatchingStage(MapperStage):
    def __init__(self, name: str, max_timespan: float, max_units: int):
        super().__init__(name)
        self.__max_timespan = max_timespan
        self.__max_units = max_units
        self.__current_batch = None
        self.__batch_start_ts = None

    def __initialize_batch(self):
        self.__current_batch = []
        self.__batch_start_ts = time()

    def __should_close_batch(self):
        units_reached = self.__max_units and len(self.__current_batch) >= self.__max_units
        timespan_reached = self.__max_timespan and (time() - self.__batch_start_ts) >= self.__max_timespan
        return units_reached or timespan_reached

    def will_start(self):
        self.__initialize_batch()

    def map(self, unit: WorkUnit):
        self.__current_batch.append(unit.payload)
        if self.__should_close_batch():
            yield WorkUnit(payload=self.__current_batch)
            self.__initialize_batch()

class MuxerStage(PipeStage):
    def work(self):
        pass

class DemuxerStage(PipeStage):
    def work(self):
        pass

class SinkStage(PipeStage):
    def __init__(self, name: str, consumer: callable = None):
        super().__init__(name)
        self.__consumer = consumer
        self.input = InputPort("input", self)
    
    def ports(self):
        yield self.input

    def consume(self, unit: WorkUnit):
        self.__consumer(unit)

    def work(self):
        while True:
            work = self.input.get()
            self.consume(work)
            self.input.task_done()
            self.work_done()

