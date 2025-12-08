"""Day 8 solver."""

import dataclasses
import functools
import heapq
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parents: list[int] = list(range(n))
        self.sizes: list[int] = [1] * n
        self.components: int = n

    def find(self, x: int) -> int:
        while x != self.parents[x]:
            self.parents[x] = x = self.parents[self.parents[x]]

        return x

    def union(self, x: int, y: int) -> None:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return

        if self.sizes[x] < self.sizes[y]:
            x, y = y, x

        self.components -= 1
        self.sizes[x] += self.sizes[y]
        self.parents[y] = x


@dataclasses.dataclass
class Point:
    x: int
    y: int
    z: int


class Solver(base.Solver):
    """Day 8 solver."""

    _cache_limit: int = 1

    def _distance(self, /, a: Point, b: Point) -> int:
        """Calculates the square distance between two points.

        Args:
            a: The first point.
            b: The second point.

        Returns:
            The squared distance between the two points.
        """
        # Unrolling is faster than using sum and zip
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2

    @functools.lru_cache(_cache_limit)
    def _parse_inputs(
        self, filepath: pathlib.Path
    ) -> tuple[list[Point], list[tuple[int, int, int]]]:
        """Parses the input.

        Args:
            filepath: The input filepath.

        Returns:
            A tuple with the:
                - List of points.
                - List of edges and its base points.
        """
        points: list[Point] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                x, y, z = (int(x) for x in line.strip().split(","))
                points.append(Point(x, y, z))

        edges = [
            (self._distance(points[i], points[j]), i, j)
            for i in range(len(points))
            for j in range(i)
        ]

        return points, edges

    @override
    def part_1(self, filepath: pathlib.Path, pairs: int = 1000) -> int | str:
        points, edges = self._parse_inputs(filepath)
        uf = UnionFind(len(points))

        edges = heapq.nsmallest(pairs, edges)
        for _, i, j in edges:
            uf.union(i, j)

        circuits = {uf.find(i) for i in range(len(points))}
        a, b, c = heapq.nlargest(3, (uf.sizes[x] for x in circuits))
        return a * b * c

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        points, edges = self._parse_inputs(filepath)
        uf = UnionFind(len(points))

        result = 0

        heapq.heapify(edges)
        while uf.components > 1:
            _, i, j = heapq.heappop(edges)
            uf.union(i, j)
            result = points[i].x * points[j].x

        return result
