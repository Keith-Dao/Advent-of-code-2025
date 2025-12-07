"""Day 7 solver."""

import collections
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 7 solver."""

    def _generic_solve(self, filepath: pathlib.Path) -> tuple[dict[int, int], int]:
        """Generic solver for both parts.

        Args:
            filepath: The input filepath.

        Returns:
            Tuple with:
                - The final positions mapped to its count.
                - The number of splitters used.
        """
        start_char = "S"
        splitter_char = "^"
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.readline().strip()
            positions: dict[int, int] = {line.index(start_char): 1}
            splits = 0

            for line in file:
                line = line.strip()
                new_positions: dict[int, int] = collections.Counter()
                for position, count in positions.items():
                    if not 0 <= position < len(line) or line[position] != splitter_char:
                        new_positions[position] += count
                        continue

                    splits += 1
                    new_positions[position - 1] += count
                    new_positions[position + 1] += count

                positions = new_positions

        return positions, splits

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        _, splits = self._generic_solve(filepath)
        return splits

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        positions, _ = self._generic_solve(filepath)
        return sum(positions.values())
