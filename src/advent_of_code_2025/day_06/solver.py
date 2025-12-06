"""Day 6 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 6 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        values: list[list[str]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                line = line.strip()
                values.append(line.split())

        def apply(operation: str, column: int) -> int:
            result = 1 if operation == "*" else 0
            for i in range(m - 1):
                if operation == "*":
                    result *= int(values[i][column])
                else:
                    result += int(values[i][column])

            return result

        result = 0
        m = len(values)
        n = len(values[0])
        for i in range(n):
            result += apply(values[m - 1][i], i)

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            lines = [line.strip("\n") for line in file]

        operators = lines[-1]
        column_ranges: list[tuple[int, int]] = []
        i = 0
        while i < len(operators):
            j = i + 1
            while j < len(operators) and operators[j] == " ":
                j += 1
            column_ranges.append((i, j - (1 if j < len(operators) else 0)))
            i = j

        m = len(lines) - 1
        result = 0

        def apply(operation: str, start: int, end: int) -> int:
            result = 1 if operation == "*" else 0

            for j in range(start, end):
                num = 0
                for i in range(m):
                    if lines[i][j] == " ":
                        continue
                    num = num * 10 + int(lines[i][j])

                if operation == "*":
                    result *= num
                else:
                    result += num

            return result

        for start, end in column_ranges:
            operation_result = apply(operators[start], start, end)
            result += operation_result

        return result
