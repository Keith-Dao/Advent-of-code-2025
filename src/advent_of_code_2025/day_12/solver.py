"""Day 12 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 12 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        def check(line: str) -> bool:
            """Checks if the blocks can be greedily placed in its own
            3x3 space.

            Args:
                line: The input line.

            Returns:
                True if each block can be placed in its own 3x3 block.
            """
            dimensions, counts = line.split(": ")
            row, col = (int(x) for x in dimensions.split("x"))
            counts = [int(x) for x in counts.split()]

            return col // 3 * row // 3 >= sum(counts)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(check(line) for line in file if "x" in line)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        return ""
