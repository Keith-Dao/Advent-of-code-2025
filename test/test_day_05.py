"""Tests day 5 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay5(BaseTests):
    """Tests the day 5 solver."""

    cases = [
        (
            textwrap.dedent("""\
                3-5
                10-14
                16-20
                12-18

                1
                5
                8
                11
                17
                32
                """),
            3,
            14,
        )
    ]
