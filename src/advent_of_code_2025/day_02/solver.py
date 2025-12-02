"""Day 2 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 2 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.read()

        result = 0
        for ranges in line.split(","):
            start, end = ranges.split("-")
            for x in range(int(start), int(end) + 1):
                s = str(x)
                if len(s) % 2 == 1:
                    continue

                if s[: len(s) // 2] == s[len(s) // 2 :]:
                    result += x

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.read()

        result = 0
        for ranges in line.split(","):
            start, end = ranges.split("-")
            for x in range(int(start), int(end) + 1):
                s = str(x)
                for i in range(1, len(s) // 2 + 1):
                    if all(s[:i] == s[j : j + i] for j in range(i, len(s), i)):
                        result += x
                        break

        return result
