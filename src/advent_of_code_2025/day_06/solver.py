"""Day 6 solver."""

import itertools
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib
    from typing import Callable

from .. import base


class Solver(base.Solver):
    """Day 6 solver."""

    def _parse_input(
        self, filepath: pathlib.Path, transpose: bool
    ) -> tuple[list[list[int]], list[str]]:
        """Parses the input file into a list of number groups and operators.

        Args:
            filepath: The path to the input file.
            transpose: If True, transposes the number groups after parsing.

        Returns:
            A tuple containing:
                - A list of lists of integers, where each inner list represents a
                  group of numbers.
                - A list of strings representing the group's respective operator.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            *values, operators = (line.strip("\n") for line in file)

            prev = 0
            groups: list[list[str]] = []
            while prev < len(operators):
                i = prev + 1
                while i < len(operators) and operators[i] == " ":
                    i += 1

                # Account for mismatched line lengths
                slice_range = slice(prev, i - 1 if i < len(operators) else None)
                groups.append([row[slice_range] for row in values])

                prev = i

            if transpose:
                groups = [
                    [
                        "".join(transposed_group)
                        for transposed_group in itertools.zip_longest(
                            *group, fillvalue=" "
                        )
                    ]
                    for group in groups
                ]

            numbers = [
                [int("".join(c for c in value if c != " ")) for value in group]
                for group in groups
            ]
            operators = operators.split()

            return numbers, operators

    def _generic_solve(self, filepath: pathlib.Path, transpose: bool) -> int:
        """Generic solve for both parts.

        Args:
            filepath: The path to the input file.
            transpose: If True, the numbers are processed as transposed,
                       otherwise as untransposed

        Returns:
            The sum of the results after applying operations to each number group.
        """

        def apply(numbers: list[int], operator: str) -> int:
            """Applies the operation to the group.

            Args:
                numbers: The numbers in the group.
                operator: The operator type to apply to the group.

            Returns:
                The result of applying the operation to the group.
            """
            operation_map: dict[str, Callable[[int, int], int]] = {
                "+": lambda x, y: x + y,
                "*": lambda x, y: x * y,
            }
            operation_start: dict[str, int] = {
                "+": 0,
                "*": 1,
            }
            result = operation_start[operator]
            operation = operation_map[operator]

            for x in numbers:
                result = operation(result, x)

            return result

        numbers, operators = self._parse_input(filepath, transpose=transpose)
        return sum(apply(*args) for args in zip(numbers, operators))

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, transpose=False)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        return self._generic_solve(filepath, transpose=True)
