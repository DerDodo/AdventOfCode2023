import copy
from typing import Tuple

from util.file_util import read_input_file


class Range:
    source: int
    destination: int
    length: int

    def __init__(self, destination: int, source: int, length: int):
        self.destination = destination
        self.source = source
        self.length = length

    def get_last(self):
        return self.source + self.length - 1


class SeedRange:
    start: int
    length: int
    is_planted: bool

    def __init__(self, start: int, length: int, is_planted: bool):
        self.start = start
        self.length = length
        self.is_planted = is_planted

    def get_last(self):
        return self.start + self.length - 1


def level5() -> Tuple[int, int]:
    seeds, range_maps = parse_input_file()
    results = copy.deepcopy(seeds)
    for range_map in range_maps:
        results = transform_seeds_with_ranges(results, range_map)
    min_location_part1 = min(results)

    seed_ranges = construct_seed_ranges(seeds)
    max_number = seed_ranges[-1].start + seed_ranges[-1].length
    range_maps = fill_ranges(range_maps, max_number)

    result_ranges = copy.deepcopy(seed_ranges)
    for range_map in range_maps:
        result_ranges = transform_ranges_with_ranges(result_ranges, range_map)

    min_location_part2 = 0
    for result_range in result_ranges:
        if result_range.is_planted:
            min_location_part2 = result_range.start
            break

    return min_location_part1, min_location_part2


def parse_input_file() -> Tuple[list[int], list[list[Range]]]:
    lines = read_input_file(5)
    seeds = list(map(int, lines[0].split(" ")[1:]))
    range_maps = list()
    current_map = list()
    for line in lines[3:]:
        if line == "":
            range_maps.append(sort_range_map(current_map))
            current_map = list()
        elif line[0].isdigit():
            parts = line.split(" ")
            current_map.append(Range(int(parts[0]), int(parts[1]), int(parts[2])))
    range_maps.append(sort_range_map(current_map))
    return seeds, range_maps


def sort_range_map(source: list[Range]) -> list[Range]:
    return sorted(source, key=lambda r: r.source, reverse=False)


def transform_seeds_with_ranges(source_list: list[int], ranges: list[Range]):
    results = list()
    for source_number in source_list:
        found = False
        for test_range in ranges:
            if test_range.source <= source_number < test_range.source + test_range.length:
                results.append(test_range.destination + source_number - test_range.source)
                found = True
                break
        if not found:
            results.append(source_number)
    return results


def fill_ranges(range_maps: list[list[Range]], max_number: int) -> list[list[Range]]:
    for range_map in range_maps:
        range_additions = list()
        new_range_start = 0
        for next_range in range_map:
            if next_range.source > new_range_start:
                range_additions.append(Range(new_range_start, new_range_start, next_range.source - new_range_start))
            new_range_start = next_range.source + next_range.length
        if new_range_start < max_number:
            range_additions.append(Range(new_range_start, new_range_start, max_number - new_range_start))
        range_map.extend(range_additions)
    range_maps = list(map(lambda r: sorted(r, key=lambda sort_range: sort_range.source), range_maps))
    return range_maps


def construct_seed_ranges(seeds: list[int]) -> list[SeedRange]:
    seed_ranges = list()
    for i in range(0, int(len(seeds) / 2)):
        seed_ranges.append(SeedRange(seeds[i * 2], seeds[i * 2 + 1], True))
    seed_ranges.sort(key=lambda r: r.start)
    max_number = seed_ranges[-1].start + seed_ranges[-1].length
    seed_range_additions = list()
    new_seed_range_start = 0
    for next_seed_range in seed_ranges:
        if next_seed_range.start > new_seed_range_start:
            seed_range_additions.append(
                SeedRange(new_seed_range_start, next_seed_range.start - new_seed_range_start, False))
        new_seed_range_start = next_seed_range.start + next_seed_range.length
    if new_seed_range_start < max_number:
        seed_range_additions.append(SeedRange(new_seed_range_start, max_number - new_seed_range_start, False))
    seed_ranges.extend(seed_range_additions)
    seed_ranges.sort(key=lambda r: r.start)
    return seed_ranges


def transform_ranges_with_ranges(source_ranges: list[SeedRange], transform_ranges: list[Range]):
    results = list()
    for source_range in source_ranges:
        transform_start = source_range.start
        transform_end = source_range.get_last()
        for transform_range in transform_ranges:
            if transform_range.source <= transform_start <= transform_range.get_last():
                if transform_end <= transform_range.get_last():
                    # fully covered
                    new_start = transform_range.destination + transform_start - transform_range.source
                    results.append(SeedRange(new_start,
                                             transform_end - transform_start + 1,
                                             source_range.is_planted))
                    break
                else:
                    # partly covered
                    new_start = transform_range.destination + transform_start - transform_range.source
                    results.append(SeedRange(new_start,
                                             transform_range.get_last() - transform_start + 1,
                                             source_range.is_planted))
                    transform_start = transform_range.get_last() + 1

    return sorted(results, key=lambda r: r.start)


if __name__ == '__main__':
    print("Lowest location: " + str(level5()))


def test_level5():
    assert (35, 0) == level5()
