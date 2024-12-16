import math
import queue
from abc import abstractmethod
from enum import Enum

from util.file_util import read_input_file
from util.run_util import RunTimer


BROADCASTER_MODULE = "broadcaster"


class PulseType(Enum):
    Low = 0
    High = 1


class ModuleInterface:
    name: str
    targets: list[str]
    sources: set[str]

    def __init__(self, line: str):
        parts = line.replace(",", "").split(" ")
        self.name = parts[0]
        self.targets = parts[2:]
        self.sources = set()

    def finish_init(self, all_modules: dict):
        for module in all_modules:
            if self.name in all_modules[module].targets:
                self.sources.add(all_modules[module].name)

    @abstractmethod
    def receive_pulse(self, pulse: PulseType, source: str) -> PulseType | None:
        pass


class FlipFlopModule(ModuleInterface):
    is_on: bool

    def __init__(self, line: str):
        super().__init__(line)
        self.is_on = False

    def receive_pulse(self, pulse: PulseType, source: str) -> PulseType | None:
        if pulse == PulseType.Low:
            self.is_on = not self.is_on
            return PulseType.High if self.is_on else PulseType.Low
        else:
            return None


class ConjunctionModule(ModuleInterface):
    stored_sources: dict[str, PulseType]

    def __init__(self, line: str):
        super().__init__(line)
        self.stored_sources = {}

    def finish_init(self, all_modules: dict):
        super().finish_init(all_modules)
        for module in all_modules:
            if self.name in all_modules[module].targets:
                self.stored_sources[all_modules[module].name] = PulseType.Low

    def receive_pulse(self, pulse: PulseType, source: str) -> PulseType | None:
        self.stored_sources[source] = pulse
        for source_pulse in self.stored_sources.values():
            if source_pulse == PulseType.Low:
                return PulseType.High
        return PulseType.Low


class BroadcastModule(ModuleInterface):
    def __init__(self, line: str):
        super().__init__(line)

    def receive_pulse(self, pulse: PulseType, source: str) -> PulseType | None:
        return pulse


class TestingModule(ModuleInterface):
    def __init__(self, name: str):
        super().__init__(f"{name} -> ")

    def receive_pulse(self, pulse: PulseType, source: str) -> PulseType | None:
        return None


module_dict = {
    "%": FlipFlopModule,
    "&": ConjunctionModule,
    "b": BroadcastModule
}


def create_module(line: str) -> ModuleInterface:
    module_line = line if line[0] == "b" else line[1:]
    return module_dict[line[0]](module_line)


def parse_input_file(file_id) -> dict[str, ModuleInterface]:
    lines = read_input_file(20, file_id)
    modules = map(create_module, lines)
    return {m.name: m for m in modules}


def init_testing_modules(modules: dict[str, ModuleInterface]):
    testing_modules = set()
    for module in modules:
        modules[module].finish_init(modules)
        for target in modules[module].targets:
            if target not in modules:
                testing_modules.add(target)

    for testing_module in testing_modules:
        modules[testing_module] = TestingModule(testing_module)


def init_high_pulses(modules: dict[str, ModuleInterface]) -> dict[str, int]:
    high_pulse = dict()
    for module in modules.values():
        if "rx" in module.targets:
            for source in module.sources:
                module_of_interest = next(filter(lambda m: source in m.targets, modules.values()))
                high_pulse[module_of_interest.name] = -1
    return high_pulse


def level20(file_id: int = 0) -> tuple[int, int]:
    modules = parse_input_file(file_id)
    init_testing_modules(modules)

    num_pulses = { PulseType.Low: 0, PulseType.High: 0 }
    high_pulse = init_high_pulses(modules)

    i = 0
    pulse_product = 0
    while pulse_product == 0 or -1 in high_pulse.values():
        pulse_queue = queue.Queue()
        pulse_queue.put((PulseType.Low, [BROADCASTER_MODULE], "button"))

        while not pulse_queue.empty():
            pulse, targets, source = pulse_queue.get()
            num_pulses[pulse] += len(targets)
            for target in targets:
                new_pulse = modules[target].receive_pulse(pulse, source)
                if new_pulse:
                    pulse_queue.put((new_pulse, modules[target].targets, modules[target].name))
                    if new_pulse == PulseType.High and source in high_pulse and high_pulse[source] == -1:
                        high_pulse[source] = i + 1

        i += 1
        if i == 1000:
            pulse_product = num_pulses[PulseType.Low] * num_pulses[PulseType.High]

    rx_trigger_once = math.lcm(*high_pulse.values()) if len(high_pulse) > 0 else 0
    return pulse_product, rx_trigger_once


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Sum part rating: {level20()}")
    timer.print()


def test_level20():
    assert (level20(0)) == (32000000, 0)
    assert (level20(1)) == (11687500, 0)
