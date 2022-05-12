import logging
import os
import re

import pytest
from licensecheck.__main__ import main

from . import create_sources_file
from . import get_args


def test_golicensecheck_license_bsd2clause(capsys):
    args = get_args('BSD-2-Clause', 'golicensecheck', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert re.match(
        r"\[license\] Detected license\(s\) .*, but set is 'BSD-2-Clause'", captured.out, re.MULTILINE)


def test_golicensecheck_license_x(capsys):
    args = get_args('X', 'golicensecheck', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert re.match(
        r"\[license\] Detected license\(s\) .*, but set is 'X'", captured.out, re.MULTILINE)


def test_golicensecheck_license_expand(capsys):
    args = get_args('GPL-2.0+', 'golicensecheck', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert re.match(
        r"\[license\] Detected license\(s\) .*, but set is 'GPL-2.0\+'", captured.out, re.MULTILINE)


def test_golicensecheck_good(capsys):
    args = get_args('BSD-3-Clause & BitTorrent-1.0 & Frameworx-1.0 & GPL-2.0 & GPL-3.0 & LGPL-2.0 & LGPL-2.1 & MIT & OLDAP-2.7 & OLDAP-2.8 & OpenSSL & curl',
                    'golicensecheck', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert '[license] Detected license(s)' not in captured.out
