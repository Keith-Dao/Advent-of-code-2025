"""Advent of code 2025 solver CLI."""

import argparse
import dataclasses
import importlib
import pathlib
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from . import base


@dataclasses.dataclass
class Args:
    day: str
    input: pathlib.Path


def parse_args() -> Args:
    """Parses the CLI args.

    Retruns:
        The parsed args.
    """

    def day(x: str) -> str:
        """Validates a day and formats it to a two-digit string.

        If the day is valid and the day is single digit, a leading
        zero is added.

        Args:
            x: The input day.

        Returns:
            A two-character string of the validated day.
        Raises:
            argparse.ArgumentTypeError: If the input day is not a number
                or not in [1, 25].
        """
        if not x.isnumeric():
            raise argparse.ArgumentTypeError(f"The day must be a number. Got: {x}")

        if not 1 <= int(x) <= 25:
            raise argparse.ArgumentTypeError(
                f"The day must be a number within the range [1, 25]. Got: {x}"
            )

        return f"{x:0>2}"

    parser = argparse.ArgumentParser(
        description="Advent of code 2025 solver.",
        usage="%(prog)s <day> [--input INPUT]",
    )

    _ = parser.add_argument(
        "day",
        type=day,
        help="The day to run the solver for.",
    )
    _ = parser.add_argument(
        "--input",
        "-i",
        type=pathlib.Path,
        help="Path to the input file.",
    )

    args = parser.parse_args()
    return Args(
        day=cast("str", args.day),
        input=cast("pathlib.Path", args.input),
    )


def get_solver(day: str) -> type[base.Solver]:
    """Gets the solver for the given day.

    Args:
        day: The day of the solver to get.

    Returns:
        The solver class.
    """
    module = importlib.import_module(f".day_{day}.solver", __name__)
    return cast("type[base.Solver]", getattr(module, "Solver"))


def main() -> None:
    args = parse_args()
    _ = get_solver(args.day)(args.input)
