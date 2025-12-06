"""Tests day 6 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay6(BaseTests):
    """Tests the day 6 solver."""

    cases = [
        (
            textwrap.dedent("""\
                123 328  51 64 
                 45 64  387 23 
                  6 98  215 314
                *   +   *   +  
                """),
            4277556,
            3263827,
        )
    ]
