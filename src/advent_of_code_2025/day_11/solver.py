"""Day 11 solver."""

import collections
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Generator
    import pathlib

from .. import base


class Solver(base.Solver):
    """Day 11 solver."""

    def _get_source_and_destinations(
        self, filepath: pathlib.Path
    ) -> Generator[tuple[str, list[str]]]:
        """Parses the input yielding the source and destinations from
        each input line.

        Args:
            filepath: The input filepath.

        Yields:
            A tuple with:
                - The source node.
                - The list of destination nodes.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                source, destinations = line.strip().split(": ")
                yield source, destinations.split()

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        graph: dict[str, list[str]] = dict(self._get_source_and_destinations(filepath))

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
        nodes: list[str] = ["out"]
        graph: dict[str, list[str]] = collections.defaultdict(list)
        degrees: dict[str, int] = collections.Counter()
        for source, destinations in self._get_source_and_destinations(filepath):
            nodes.append(source)
            for destination in destinations:
                graph[destination].append(source)
                degrees[source] += 1

        node_to_index = {node: i for i, node in enumerate(nodes)}
        dp = [[0] * 4 for _ in range(len(nodes))]
        dp[node_to_index["out"]][0b11] = 1
        stack = ["out"]

        while stack:
            node = stack.pop()
            for prev_node in graph[node]:
                if prev_node == "dac":
                    mask = 1
                elif prev_node == "fft":
                    mask = 1 << 1
                else:
                    mask = 0

                for state in range(4):
                    dp[node_to_index[prev_node]][state] += dp[node_to_index[node]][
                        state | mask
                    ]

                degrees[prev_node] -= 1
                if degrees[prev_node] == 0:
                    stack.append(prev_node)

        return dp[node_to_index["svr"]][0]
