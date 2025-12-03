"""Day 3 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 3 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        result = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                best = past = 0
                for c in line.strip():
                    x = int(c)
                    best = max(best, past * 10 + x)
                    past = max(past, x)

                result += best

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        result = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                stack: list[int] = []
                line = line.strip()
                n = len(line)
                for i, c in enumerate(line):
                    x = int(c)
                    while stack and len(stack) + n - i > 12 and x > stack[-1]:
                        _ = stack.pop()

                    if len(stack) < 12:
                        stack.append(x)

                num = 0
                for x in stack:
                    num = num * 10 + x
                result += num

        return result
