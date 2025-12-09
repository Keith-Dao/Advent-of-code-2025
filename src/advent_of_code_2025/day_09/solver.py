"""Day 9 solver."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 9 solver."""

    def _area(self, /, a: tuple[int, int], b: tuple[int, int]) -> int:
        return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

    def _is_valid(self, points: list[tuple[int, int]], i: int, j: int) -> bool:
        left = min(points[i][0], points[j][0])
        right = max(points[i][0], points[j][0])
        top = min(points[i][1], points[j][1])
        bottom = max(points[i][1], points[j][1])

        n = len(points)
        for k in range(n):
            a = points[k]
            b = points[(k + 1) % n]
            if (
                a[0] == b[0]
                and left < a[0] < right
                and not (max(a[1], b[1]) <= top or bottom <= min(a[1], b[1]))
            ):
                return False
            if (
                a[1] == b[1]
                and top < a[1] < bottom
                and not (max(a[0], b[0]) <= left or right <= min(a[0], b[0]))
            ):
                return False

        return True

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        points: list[tuple[int, int]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                line = line.strip()
                x, y = line.split(",")
                points.append((int(x), int(y)))

        return max(
            self._area(points[i], points[j])
            for i in range(len(points))
            for j in range(i)
        )

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        points: list[tuple[int, int]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                line = line.strip()
                x, y = line.split(",")
                points.append((int(x), int(y)))

        return max(
            self._area(points[i], points[j])
            for i in range(len(points))
            for j in range(i)
            if self._is_valid(points, i, j)
        )
