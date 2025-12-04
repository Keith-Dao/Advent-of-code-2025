"""Day 2 solver."""

import bisect
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 2 solver."""

    def _parse_input(self, filepath: pathlib.Path) -> Generator[tuple[int, int]]:
        """Parses the input.

        Args:
            filepath: The input filepath.

        Yields:
            The start and end of the range inclusively.
        """
        result = [0, 0]
        i = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            char = file.read(1)
            while char != "":
                if char == ",":
                    yield result[0], result[1]
                    result = [0, 0]
                    i = 0
                elif char.isdigit():
                    result[i] = result[i] * 10 + int(char)
                else:
                    i += 1

                char = file.read(1)

        yield result[0], result[1]

    def _make_intervals(self, filepath: pathlib.Path) -> list[tuple[int, int]]:
        """Makes the intervals array from the input.

        Args:
            filepath: The input filepath.

        Returns:
            The sorted invervals array.
        """
        return sorted(interval for interval in self._parse_input(filepath))

    def _generate_invalid_nums(
        self, max_num: int, repeat_once: bool = False
    ) -> Generator[int]:
        """Generates all invalid numbers up to and including the maximum number.

        Args:
            max_num: The maximum number in the input.
            repeat_once: If true, only supply numbers that have a subsequence
                that repeats once. If false, the subsequence can repeat multiple
                times.

        Yields:
            A number that has a repeated subsequence.
        """
        used: set[int] = set()
        start_num = 1
        mask = start_num * 10 + 1
        while mask * start_num <= max_num:  # Control subsequence length
            while mask * start_num <= max_num:  # Control number of repeats
                for sequence in range(start_num, start_num * 10):
                    num = sequence * mask
                    if num > max_num:
                        break

                    if num in used:
                        continue

                    used.add(num)
                    yield num

                if repeat_once:
                    break

                mask = mask * start_num * 10 + 1

            start_num *= 10
            mask = start_num * 10 + 1

    def _generic_solve(
        self, filepath: pathlib.Path, repeat_subsequence_once: bool
    ) -> int:
        """Generic solver for both parts.

        Args:
            filepath: The input filepath.
            repeat_once: If true, only check numbers that have a subsequence
                that repeats once. If false, check numbers where the subsequence can repeat
                multiple times.

        Returns:
            The solution to the problem.
        """
        intervals = self._make_intervals(filepath)
        max_num = intervals[-1][1]

        result = 0
        for num in self._generate_invalid_nums(
            max_num, repeat_once=repeat_subsequence_once
        ):
            i = bisect.bisect_left(intervals, num, key=lambda interval: interval[1])
            if intervals[i][0] <= num <= intervals[i][1]:
                result += num

        return result

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, repeat_subsequence_once=True)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, repeat_subsequence_once=False)
