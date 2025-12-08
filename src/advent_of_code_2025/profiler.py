"""This module contains the profiler wrapper."""

import cProfile
import functools
import io
import pstats
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from typing import Callable

P = ParamSpec("P")
R = TypeVar("R")


def profile(func: Callable[P, R]) -> Callable[P, R]:
    """Profiles a function.

    Args:
        func: The function to profile.

    Returns:
        A decorator to profile a function.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        with cProfile.Profile() as pr:
            result = func(*args, **kwargs)

            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            _ = ps.print_stats()
            print(s.getvalue())

        return result

    return wrapper
