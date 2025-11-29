"""Base test."""

import importlib
import inspect
import pathlib
import sys
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from advent_of_code_2025.base import Solver


class BaseTests:
    """Base tests"""

    cases: list[tuple[str, int | str | None, int | str | None]]
    test_args: dict[str, Any] | None
    ignore_args: tuple[list[str], list[str]]

    # === Test cases ===
    def pytest_generate_tests(self, metafunc: pytest.Metafunc):
        """Pytest runs this before tests are run. Tests cases are
        generated using the case attributes.

        Args:
            metafunc: The test function.
        """
        test_cases = [
            (i, (input_file, solution, part))
            for i, (input_file, *solutions) in enumerate(self.cases)
            for part, solution in enumerate(solutions, start=1)
            if solution is not None
        ]

        metafunc.parametrize(
            ["input_file", "solution", "part"],
            [param for _, param in test_cases],
            indirect=["input_file"],
            ids=[f"Test {test_id} - part {part}" for test_id, (*_, part) in test_cases],
        )

    # === Fixtures ===
    @pytest.fixture
    def input_file(
        self,
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> pathlib.Path:
        """Creates a temporary input file with the test input.

        Args:
            tmp_path: The temporary path to store the input file.

        Returns:
            Path to the temporary input file.
        """
        input_data = request.param
        input_file = tmp_path / "input.txt"
        with open(input_file, "w", encoding=sys.getdefaultencoding()) as file:
            file.write(input_data)

        return input_file

    @pytest.fixture
    def solver(self) -> Solver:
        """Gets the solver for the testing day.

        Returns:
            The solver for the day to be tested.
        """
        test_module = inspect.getmodule(self)
        day = test_module.__name__[-2:]

        module = importlib.import_module(f"advent_of_code_2025.day_{day}.solver")
        solver = getattr(module, "Solver")

        return solver()

    # === Tests ===
    def test_part(
        self,
        solver: Solver,
        input_file: pathlib.Path,
        solution: int,
        part: int,
    ):
        """Tests a part of the solver."""
        test_args = getattr(self, "test_args", {})
        ignore_args = getattr(self, "ignore_args", ([], []))[part - 1]
        for ignore_arg in ignore_args:
            test_args.pop(ignore_arg)

        assert getattr(solver, f"part_{part}")(input_file, **test_args) == solution
