"""Day 5 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    from io import TextIOWrapper
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 5 solver."""

    def _get_intervals(self, file: TextIOWrapper) -> Generator[tuple[int, int]]:
        """Yields the intervals in the input.

        Args:
            file: The opened input file.

        Yields:
            The start and end interval inclusive.
        """
        line = file.readline().strip()
        while line != "":
            start, end = (int(x) for x in line.split("-"))
            yield start, end
            line = file.readline().strip()

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        intervals: list[list[int]] = []
        result: int = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for start, end in self._get_intervals(file):
                intervals.append([start, end])

            for line in file:
                line = line.strip()
                x = int(line)
                result += any(start <= x <= end for start, end in intervals)

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        intervals: list[list[int]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for start, end in self._get_intervals(file):
                intervals.append([start, end])

        merged_intervals: list[list[int]] = []

        for start, end in sorted(intervals):
            if merged_intervals and start <= merged_intervals[-1][1]:
                merged_intervals[-1][1] = max(merged_intervals[-1][1], end)
            else:
                merged_intervals.append([start, end])

        return sum(end - start + 1 for start, end in merged_intervals)
