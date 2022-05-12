import pytest
from license_expression import Licensing

from . import get_args


def test_clean_expression():
    from licensecheck_helper.licensecheck import clean_expression

    for k, v in {
        'BSD-2-Clause': ['BSD-2-Clause'],
        ' ': [],
        'BSD-2-Clause AND BSD-2-Clause': ['BSD-2-Clause'],
        'BSD-2-Clause OR BSD-2-Clause': ['BSD-2-Clause'],
    }.items():
        _lic = Licensing().parse(k)
        if _lic is not None:
            _lic = _lic.simplify()
            _lic = str(_lic)
        assert clean_expression(_lic) == v


def test_no_version_info(caplog):
    from licensecheck_helper.provider import Provider
    from licensecheck_helper.licensecheck import evaluate
    from licensecheck_helper.__main__ import create_parser

    _args = create_parser(get_args('BSD-2-Clause', 'lc', ['test2/test-2.sh']))

    evaluate(_args, Provider(_args))

    assert any("Can't find any license info" in x.message for x in caplog.records)
