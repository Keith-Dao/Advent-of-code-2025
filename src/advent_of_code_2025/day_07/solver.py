"""Day 7 solver."""

import collections
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 7 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        result = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.readline().strip()
            positions: set[int] = {line.index("S")}
            for line in file:
                line = line.strip()
                new_positions: set[int] = set()
                for position in positions:
                    if not 0 <= position < len(line) or line[position] != "^":
                        new_positions.add(position)
                        continue

                    result += 1
                    new_positions.add(position - 1)
                    new_positions.add(position + 1)

                positions = new_positions

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.readline().strip()
            positions: dict[int, int] = collections.Counter([line.index("S")])
            for line in file:
                line = line.strip()
                new_positions: dict[int, int] = collections.Counter()
                for position, count in positions.items():
                    if not 0 <= position < len(line) or line[position] != "^":
                        new_positions[position] += count
                        continue

                    new_positions[position - 1] += count
                    new_positions[position + 1] += count

                positions = new_positions

        return sum(positions.values())
