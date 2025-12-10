"""Day 10 solver."""

import collections
import sys
from typing import TYPE_CHECKING, cast, override

import scipy.optimize

if TYPE_CHECKING:
    import pathlib
    from typing import Literal


from .. import base


class Solver(base.Solver):
    """Day 10 solver."""

    def _parse_line(self, line: str) -> tuple[int, list[set[int]], list[int]]:
        """Parses the input line.

        Args:
            line: The input line.

        Returns:
            A tuple with:
                - The binary mask of the indicator lights.
                    Each bit represents whether a light is on (1)
                        or off (0).
                    The bits are read right to left.
                - The buttons with each set representing
                    the set of indices it toggles..
                - The target values for the position counter.
        """
        line = line.strip()
        indicator, *buttons, counter = line.split()

        indicator_state = 0
        for i, c in enumerate(indicator[1:-1]):
            if c == ".":
                continue

            indicator_state |= 1 << i

        buttons = [{int(x) for x in button[1:-1].split(",")} for button in buttons]

        counter = [int(x) for x in counter[1:-1].split(",")]

        return indicator_state, buttons, counter

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        def solve(line: str) -> int:
            """Gets the minimum number of button presses
            to reach the desired state in the input line.

            Args:
                line: The input line.

            Returns:
                The minimum number of button presses to
                reach the desired state.
            """
            target, buttons, _ = self._parse_line(line)

            toggles: set[int] = set()
            for button in buttons:
                toggle = 0
                for i in button:
                    toggle ^= 1 << i

                toggles.add(toggle)

            num_bits = max(max(button) for button in buttons) + 1

            visited = [False] * (1 << num_bits)
            visited[0] = True
            queue = collections.deque([0])
            depth = 1
            while queue:
                for _ in range(len(queue)):
                    state = queue.popleft()

                    for toggle in toggles:
                        next_state = state ^ toggle
                        if next_state == target:
                            return depth

                        if visited[next_state]:
                            continue

                        visited[next_state] = True
                        queue.append(next_state)

                depth += 1

            raise ValueError("Target state was never reached")

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(solve(line) for line in file)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        def solve(line: str) -> int:
            """Gets the minimum number of button presses
            to reach the desired counts in the input line.

            Args:
                line: The input line.

            Returns:
                The minimum number of button presses to
                reach the desired counts.
            """
            _, buttons, target = self._parse_line(line)

            weights: list[Literal[1]] = [1] * len(buttons)
            variable_type: list[Literal[1]] = [1] * len(buttons)
            button_matrix = [
                [i in button for button in buttons] for i in range(len(target))
            ]
            milp_result: scipy.optimize.OptimizeResult = scipy.optimize.milp(
                weights,
                integrality=variable_type,
                constraints=(
                    scipy.optimize.LinearConstraint(
                        button_matrix, lb=target, ub=target
                    ),
                ),
            )
            return int(cast("float", milp_result.fun))

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(solve(line) for line in file)
