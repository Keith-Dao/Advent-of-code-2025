"""This module contains the base solver."""

import abc
import inspect
import pathlib


class Solver(abc.ABC):
    """Base solver."""

    @abc.abstractmethod
    def part_1(self, filepath: pathlib.Path) -> int | str:
        """
        Solves part 1.

        Args:
            filepath: The path to the data file.

        Returns:
            The solution to part 1.
        """

    @abc.abstractmethod
    def part_2(self, filepath: pathlib.Path) -> int | str:
        """
        Solves part 2.

        Args:
            filepath: The path to the data file.

        Returns:
            The solution to part 2.
        """

    @property
    def day(self) -> str:
        """The day of the solver."""
        solver_module = inspect.getmodule(self)
        if solver_module and solver_module.__package__:
            return solver_module.__package__[-2:].lstrip("0")

        raise ValueError("Unable to extract the day.")

    def solve(self, file: pathlib.Path) -> None:
        """
        Run the solver.

        Args:
            file: The path to the data file.
        """
        print(f"Day {self.day}")
        print("Part 1:", self.part_1(file))
        print("===========================")
        print("Part 2:", self.part_2(file))

    def __init__(self, file: pathlib.Path | None = None) -> None:
        """
        Base solver.

        Args:
            file: The path to the data file. If not provided, do nothing.
                If a file is provided, immediately solve.
        """
        if not file:
            return

        self.solve(file)
