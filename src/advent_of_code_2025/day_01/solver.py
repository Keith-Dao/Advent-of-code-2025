"""Day 1 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 1 solver."""

    def _parse_input(self, filepath: pathlib.Path) -> Generator[tuple[int, int]]:
        """Parses the input.

        Args:
            filepath: The input filepath.

        Yields:
            The amount to shift and the total number of full rotations respectively.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                negative = line[0] == "L"
                amount = int(line[1:])

                full_rotations = amount // 100
                amount %= 100
                if negative:
                    amount = -amount

                yield amount, full_rotations

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        result = 0
        current = 50

        for amount, _ in self._parse_input(filepath):
            current += amount
            current %= 100

            result += current == 0

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        result = 0
        current = 50

        for amount, full_rotations in self._parse_input(filepath):
            result += full_rotations
            result += current != 0 and (
                current + amount <= 0 or current + amount >= 100
            )

            current += amount
            current %= 100

        return result
