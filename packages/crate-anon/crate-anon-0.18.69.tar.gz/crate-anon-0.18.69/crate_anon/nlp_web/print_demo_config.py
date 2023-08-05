#!/usr/bin/env python

r"""
crate_anon/nlp_web/print_demo_config.py

===============================================================================

    Copyright (C) 2015-2019 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

Prints a demo config for CRATE's implementation of an NLPRP server.
"""

from crate_anon.nlp_web.constants import DEMO_CONFIG


def main() -> None:
    """
    Prints a config file for the NLPRP server.
    """
    print(DEMO_CONFIG)
