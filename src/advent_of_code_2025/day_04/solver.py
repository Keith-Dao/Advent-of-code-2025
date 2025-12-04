"""Day 4 solver."""

import itertools
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 4 solver."""

    ROLL: str = "@"

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            grid = [line.strip() for line in file]

        m, n = len(grid), len(grid[0])
        result = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x != self.ROLL:
                    continue

                count = 0
                for d_i, d_j in itertools.product([-1, 0, 1], repeat=2):
                    if d_i == d_j == 0:
                        continue

                    n_i = i + d_i
                    n_j = j + d_j
                    if not 0 <= n_i < m or not 0 <= n_j < n:
                        continue

                    count += grid[n_i][n_j] == self.ROLL
                    if count >= 4:
                        break

                result += count < 4

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            grid = [line.strip() for line in file]

        m, n = len(grid), len(grid[0])
        counts = [[-1] * n for _ in range(m)]
        stack: list[tuple[int, int]] = []
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x != self.ROLL:
                    continue

                count = 0
                for d_i, d_j in itertools.product([-1, 0, 1], repeat=2):
                    if d_i == d_j == 0:
                        continue

                    n_i = i + d_i
                    n_j = j + d_j
                    if not 0 <= n_i < m or not 0 <= n_j < n:
                        continue

                    count += grid[n_i][n_j] == self.ROLL

                if count < 4:
                    stack.append((i, j))
                else:
                    counts[i][j] = count

        result = 0
        while stack:
            result += 1
            i, j = stack.pop()

            for d_i, d_j in itertools.product([-1, 0, 1], repeat=2):
                if d_i == d_j == 0:
                    continue

                n_i = i + d_i
                n_j = j + d_j
                if not 0 <= n_i < m or not 0 <= n_j < n or counts[n_i][n_j] < 4:
                    continue

                counts[n_i][n_j] -= 1
                if counts[n_i][n_j] < 4:
                    counts[n_i][n_j] = -1
                    stack.append((n_i, n_j))

        return result
