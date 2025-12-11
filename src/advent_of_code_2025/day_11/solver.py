"""Day 11 solver."""

import functools
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 11 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        graph: dict[str, list[str]] = {}
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                source, destinations = line.strip().split(": ")
                graph[source] = []
                for destination in destinations.split():
                    graph[source].append(destination)

        result = 0
        stack = ["you"]
        while stack:
            node = stack.pop()
            if node == "out":
                result += 1
                continue

            for next_node in graph[node]:
                stack.append(next_node)

        return result

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        graph: dict[str, list[str]] = {}
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                source, destinations = line.strip().split(": ")
                graph[source] = []
                for destination in destinations.split():
                    graph[source].append(destination)

        @functools.cache
        def dfs(node: str, state: int) -> int:
            if node == "out":
                return int(state == 0b11)

            result = 0
            for next_node in graph[node]:
                next_state = state
                if next_node == "dac":
                    next_state |= 1
                if next_node == "fft":
                    next_state |= 1 << 1

                result += dfs(next_node, next_state)

            return result

        return dfs("svr", 0)
