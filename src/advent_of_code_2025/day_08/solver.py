"""Day 8 solver."""

import heapq
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parents: list[int] = list(range(n))
        self.ranks: list[int] = [1] * n
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

        if self.ranks[x] < self.ranks[y]:
            x, y = y, x

        self.components -= 1
        self.ranks[x] += self.ranks[y]
        self.parents[y] = x


class Solver(base.Solver):
    """Day 8 solver."""

    @override
    def part_1(self, filepath: pathlib.Path, pairs: int = 1000) -> int | str:
        points: list[tuple[int, int, int]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                x, y, z = (int(x) for x in line.strip().split(","))
                points.append((x, y, z))

        uf = UnionFind(len(points))

        def distance(i: int, j: int) -> int:
            return sum((x - y) ** 2 for x, y in zip(points[i], points[j]))

        edges = heapq.nsmallest(
            pairs,
            ((distance(i, j), i, j) for i in range(len(points)) for j in range(i)),
        )

        for _, i, j in edges:
            uf.union(i, j)

        circuits = {uf.find(i) for i in range(len(points))}
        a, b, c = heapq.nlargest(3, (uf.ranks[x] for x in circuits))
        return a * b * c

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        points: list[tuple[int, int, int]] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                x, y, z = (int(x) for x in line.strip().split(","))
                points.append((x, y, z))

        uf = UnionFind(len(points))

        def distance(i: int, j: int) -> int:
            return sum((x - y) ** 2 for x, y in zip(points[i], points[j]))

        heap = [(distance(i, j), i, j) for i in range(len(points)) for j in range(i)]
        heapq.heapify(heap)
        last = (0, 0)

        while uf.components > 1:
            _, i, j = heapq.heappop(heap)
            uf.union(i, j)
            last = (points[i][0], points[j][0])

        return last[0] * last[1]
