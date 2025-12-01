"""Tests day 1 solver."""

import textwrap

from .base_test import BaseTests


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
