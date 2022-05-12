import logging
import os

import pytest
from licensecheck.__main__ import main

from . import create_sources_file
from . import get_args


def test_lc_license_bsd2clause(capsys):
    args = get_args('BSD-2-Clause', 'lc', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'BSD-2-Clause'" in captured.out


def test_lc_license_x(capsys):
    args = get_args('X', 'lc', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'X'" in captured.out


def test_lc_license_expand(capsys):
    args = get_args('GPL-2.0+', 'lc', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'GPL-2.0+'" in captured.out


def test_lc_good(capsys):
    args = get_args('GPL-3.0', 'lc', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'GPL-3.0'" not in captured.err
