"""Day 5 solver."""

import bisect
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    import pathlib
    from typing import TextIO

from .. import base


class Solver(base.Solver):
    """Day 5 solver."""

    def _read_intervals(self, file: TextIO) -> Generator[tuple[int, int]]:
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

    def _get_intervals(self, file: TextIO) -> list[tuple[int, int]]:
        """Gets the intervals within the input.

        Args:
            file: The opened input file.

        Returns:
            The intervals with overlapping intervals merged.
        """
        unmerged_intervals = sorted(self._read_intervals(file))

        intervals: list[tuple[int, int]] = []
        for start, end in unmerged_intervals:
            if intervals and start <= intervals[-1][1]:
                intervals[-1] = intervals[-1][0], max(intervals[-1][1], end)
            else:
                intervals.append((start, end))

        return intervals

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        result: int = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            intervals = self._get_intervals(file)

            for line in file:
                line = line.strip()
                x = int(line)
                i = bisect.bisect_left(intervals, x, key=lambda x: x[1])
                result += i < len(intervals) and intervals[i][0] <= x <= intervals[i][1]

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            intervals = self._get_intervals(file)

        return sum(end - start + 1 for start, end in intervals)
