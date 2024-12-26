from collections import defaultdict

from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file() -> dict[str, list[str]]:
    lines = read_input_file(25)
    components = defaultdict(list)
    for line in lines:
        parts = line.split(": ")
        components[parts[0]] = parts[1].split(" ")

    new_components = defaultdict(list)
    for component, other_components in components.items():
        for other_component in other_components:
            new_components[other_component].append(component)
    for new_component, other_components in new_components.items():
        components[new_component].extend(other_components)

    return components


def calc_low_couplings(components: dict[str, list[str]]) -> set[tuple[str, str]]:
    low_couplings: set[tuple[str, str]] = set()
    for component, other_components in components.items():
        test_couplings = defaultdict(int)
        for other_component in other_components:
            if other_component not in test_couplings:
                test_couplings[other_component] = 0
            for next_component in components[other_component]:
                if next_component in other_components:
                    test_couplings[next_component] += 1
        for test_coupling, value in test_couplings.items():
            if value == 0:
                if test_coupling < component:
                    low_couplings.add((test_coupling, component))
                else:
                    low_couplings.add((component, test_coupling))
    return low_couplings


def level25() -> str:
    components = parse_input_file()
    couplings = list(calc_low_couplings(components))
    couplings.sort()
    return get_component_diagram(components)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Diagram: {level25()}")
    timer.print()


def test_level21():
    print(level25())
