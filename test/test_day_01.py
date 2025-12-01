"""Tests day 1 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay1(BaseTests):
    """Tests the day 1 solver."""

    cases = [
        (
            textwrap.dedent("""\
                L68
                L30
                R48
                L5
                R60
                L55
                L1
                L99
                R14
                L82
                """),
            3,
            6,
        )
    ]
