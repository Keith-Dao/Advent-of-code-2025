"""Tests day 3 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay3(BaseTests):
    """Tests the day 3 solver."""

    cases = [
        (
            textwrap.dedent("""\
                987654321111111
                811111111111119
                234234234234278
                818181911112111
                """),
            357,
            3121910778619,
        )
    ]
