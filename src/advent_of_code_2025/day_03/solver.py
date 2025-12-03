"""Day 3 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 3 solver."""

    def _generic_solve(self, filepath: pathlib.Path, sequence_length: int) -> int:
        """Generic solver for both parts.

        Args:
            filepath: The input filepath.
            sequence_length: The sequence length to extract for the problem.

        Returns:
            The solution to the problem.
        """

        def get_maximum_number_from_line(line: str) -> int:
            """Gets the maximum number for the given line.

            Args:
                line: The line to extract the score fore.

            Returns:
                The maximum number in the line.
            """
            line = line.strip()
            n = len(line)

            stack: list[int] = []
            for i, c in enumerate(line):
                x = int(c)
                while stack and len(stack) + n - i > sequence_length and x > stack[-1]:
                    _ = stack.pop()

                if len(stack) < sequence_length:
                    stack.append(x)

            num = 0
            for x in stack:
                num = num * 10 + x

            return num

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(get_maximum_number_from_line(line) for line in file)

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, 2)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, 12)
