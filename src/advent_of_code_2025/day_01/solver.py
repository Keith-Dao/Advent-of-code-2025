"""Day 1 solver."""

import pathlib
import sys

from .. import base


class Solver(base.Solver):
    """Day 1 solver."""

    def part_1(self, filepath: pathlib.Path) -> int | str:
        result = 0
        current = 50

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                negative = line[0] == "L"
                amount = int(line[1:])
                if negative:
                    amount = -amount

                current += amount
                current %= 100

                result += current == 0

        return result

    def part_2(self, filepath: pathlib.Path) -> int | str:
        result = 0
        current = 50

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                negative = line[0] == "L"
                amount = int(line[1:])

                result += amount // 100
                amount %= 100

                if negative:
                    amount = -amount

                result += current != 0 and (
                    current + amount <= 0 or current + amount >= 100
                )

                current += amount
                current %= 100

        return result
