"""Day 4 solver."""

import itertools
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 4 solver."""

    ROLL: str = "@"

    def _get_next_positions(self, i: int, j: int) -> Generator[tuple[int, int]]:
        """Generates the 8 neighboring positions (including diagonals) for a given cell.

        Args:
            i: The row index of the current cell.
            j: The column index of the current cell.

        Yields:
            The neighboring cell's coordinates.
        """
        for d_i, d_j in itertools.product([-1, 0, 1], repeat=2):
            if d_i == d_j == 0:
                continue

            yield i + d_i, j + d_j

    def _get_surrounding_counts(self, filepath: pathlib.Path) -> list[list[int]]:
        """Gets the number of surrounding rolls for each cell in the grid.

        Args:
            filepath: The input filepath.

        Returns:
            A grid matching the input file with the count of surrounding
            rolls. If the cell was not a roll, the count will be -1.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            grid = [line.strip() for line in file]

        m = len(grid)
        n = len(grid[0])

        counts = [[-1] * n for _ in range(m)]
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x != self.ROLL:
                    continue

                count = 0
                for n_i, n_j in self._get_next_positions(i, j):
                    if not 0 <= n_i < m or not 0 <= n_j < n:
                        continue

                    count += grid[n_i][n_j] == self.ROLL

                counts[i][j] = count

        return counts

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        counts = self._get_surrounding_counts(filepath)
        return sum(sum(x != -1 and x < 4 for x in row) for row in counts)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        counts = self._get_surrounding_counts(filepath)

        m = len(counts)
        n = len(counts[0])

        stack: list[tuple[int, int]] = []
        for i, row in enumerate(counts):
            for j, x in enumerate(row):
                if x == -1 or x >= 4:
                    continue

                counts[i][j] = -1
                stack.append((i, j))

        result = 0
        while stack:
            result += 1
            i, j = stack.pop()

            for n_i, n_j in self._get_next_positions(i, j):
                if not 0 <= n_i < m or not 0 <= n_j < n or counts[n_i][n_j] < 4:
                    continue

                counts[n_i][n_j] -= 1
                if counts[n_i][n_j] < 4:
                    counts[n_i][n_j] = -1
                    stack.append((n_i, n_j))

        return result
