"""Day 10 solver."""

import collections
import sys
from typing import TYPE_CHECKING, override

import z3

if TYPE_CHECKING:
    import pathlib


from .. import base


class Solver(base.Solver):
    """Day 10 solver."""

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        def solve(line: str) -> int:
            line = line.strip()
            target, *buttons, _ = line.split()

            target_state = 0
            for i, c in enumerate(target[1:-1]):
                if c == ".":
                    continue

                target_state |= 1 << i

            toggles: set[int] = set()
            for button in buttons:
                state = 0
                for c in button[1:-1].split(","):
                    state ^= 1 << int(c)
                toggles.add(state)

            visited = {0}
            queue = collections.deque([0])
            depth = 1
            while queue:
                for _ in range(len(queue)):
                    state = queue.popleft()

                    for toggle in toggles:
                        next_state = state ^ toggle
                        if next_state == target_state:
                            return depth

                        if next_state in visited:
                            continue

                        visited.add(next_state)
                        queue.append(next_state)

                depth += 1

            raise ValueError("Target state was never reached")

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(solve(line) for line in file)

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        def solve(line: str) -> int:
            line = line.strip()
            _, *buttons, target = line.split()

            buttons = [{int(x) for x in button[1:-1].split(",")} for button in buttons]

            start_state = tuple(int(x) for x in target[1:-1].split(","))

            solver = z3.Optimize()
            button_vars = [z3.Int(f"b_{i}") for i in range(len(buttons))]

            button_presses = [
                [button_vars[i] for i, button in enumerate(buttons) if j in button]
                for j in range(len(start_state))
            ]
            for button_var in button_vars:
                solver.add(button_var >= 0)

            for press, expected in zip(button_presses, start_state):
                solver.add(sum(press) == expected)

            solver.minimize(sum(button_vars))

            solver.check()
            model = solver.model()
            values = [model[button_var].as_long() for button_var in button_vars]
            return sum(values)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(solve(line) for line in file)
