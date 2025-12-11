"""Tests day 11 solver."""

import textwrap
from typing import final

from .base_test import BaseTests


@final
class TestDay11(BaseTests):
    """Tests the day 11 solver."""

    cases = [
        (
            textwrap.dedent("""\
                aaa: you hhh
                you: bbb ccc
                bbb: ddd eee
                ccc: ddd eee fff
                ddd: ggg
                eee: out
                fff: out
                ggg: out
                hhh: ccc fff iii
                iii: out"""),
            5,
            None,
        ),
        (
            textwrap.dedent("""\
                svr: aaa bbb
                aaa: fft
                fft: ccc
                bbb: tty
                tty: ccc
                ccc: ddd eee
                ddd: hub
                hub: fff
                eee: dac
                dac: fff
                fff: ggg hhh
                ggg: out
                hhh: out
                """),
            None,
            2,
        ),
    ]
