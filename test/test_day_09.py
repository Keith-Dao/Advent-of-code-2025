"""Tests day 9 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay9(BaseTests):
    """Tests the day 9 solver."""

    cases = [
        (
            textwrap.dedent("""\
                7,1
                11,1
                11,7
                9,7
                9,5
                2,5
                2,3
                7,3
                """),
            50,
            24,
        )
    ]
