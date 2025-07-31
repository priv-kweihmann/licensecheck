import logging
import os

import pytest
from licensecheck_helper.__main__ import main

from . import create_sources_file
from . import get_args


def test_scancode_v4_1_license_bsd2clause(capsys):
    args = get_args('BSD-2-Clause', 'scancode-v4.1', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'BSD-2-Clause'" in captured.out


def test_scancode_v4_1_license_x(capsys):
    args = get_args('X', 'scancode-v4.1', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'X'" in captured.out


def test_scancode_v4_1_license_expand(capsys):
    args = get_args('GPL-2.0+', 'scancode-v4.1', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'GPL-2.0+'" in captured.out


def test_scancode_v4_1_good(capsys):
    args = get_args('GPL-3.0', 'scancode-v4.1', ['test2/test-2.sh'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'GPL-3.0'" not in captured.out


def test_scancode_v4_1_crholder(capsys):
    args = get_args('GPL-3.0', 'scancode-v4.1',
                    ['jinja2/Jinja2-3.0.1/docs/conf.py'], badcrholders='Pallets')
    main(args)
    captured = capsys.readouterr()

    assert "[copyright] Detected discouraged copyright holder 'Pallets'" in captured.out


def test_scancode_v4_1_noinfo(capsys):
    args = get_args('GPL-3.0', 'scancode-v4.1',
                    ['K01speech-dispatcher'])
    main(args)
    captured = capsys.readouterr()

    assert "[noinfo] path 'K01speech-dispatcher' doesn't provide a license info" in captured.out


def test_scancode_v4_1_nospdx(capsys):
    args = get_args('GPL-3.0', 'scancode-v4.1',
                    ['curl-7.30.0.ermine/curl.ermine'])
    main(args)
    captured = capsys.readouterr()

    assert "[license] Detected license(s) GPL-3.0, but set is 'GPL-3.0'" not in captured.out


def test_scancode_v4_1_ignorepattern(capsys):
    args = get_args('X', 'scancode-v4.1',
                    ['curl-7.30.0.ermine/curl.ermine'],
                    sources=create_sources_file(
                        ['curl-7.30.0.ermine/curl.ermine']),
                    ignorelicfiles='curl-7.30.0.ermine/curl.ermine')
    main(args)
    captured = capsys.readouterr()

    assert '[license] Detected ' not in captured.out


def test_scancode_v4_1_ignorepattern2(capsys):
    args = get_args('X', 'scancode-v4.1',
                    ['curl-7.30.0.ermine/curl.ermine'],
                    sources=create_sources_file(
                        ['curl-7.30.0.ermine/curl.ermine',
                         'curl-7.30.0.ermine/another-file']),
                    ignorelicfiles='curl-7.30.0.ermine/another-file')
    main(args)
    captured = capsys.readouterr()

    assert '[license] Detected ' not in captured.out


def test_scancode_v4_1_ignorepattern2_wo_sources(capsys):
    args = get_args('X', 'scancode-v4.1',
                    ['curl-7.30.0.ermine/curl.ermine'],
                    ignorelicfiles='curl-7.30.0.ermine/another-file')
    main(args)
    captured = capsys.readouterr()

    assert '[license] Detected ' not in captured.out
