import argparse
import sys

from licensecheck_helper.logger import setup as logger_setup
from licensecheck_helper.licensecheck import _sanitize_license
from licensecheck_helper.licensecheck import evaluate
from licensecheck_helper.licensecheck import interal_comp_expression
from licensecheck_helper.provider.golicensecheck import ProviderGolicensecheck
from licensecheck_helper.provider.lc import ProviderLC
from licensecheck_helper.provider.reuse import ProviderReuse
from licensecheck_helper.provider.scancode import ProviderScancode


def create_parser(args=None):
    parser = argparse.ArgumentParser(
        description='License check', prog='licensecheck_helper')
    parser.add_argument('--noassertdefault', default='CLOSED',
                        help='In case no assertion can be made on a file, take this license as the basis')
    parser.add_argument('--badcrholders', default='',
                        help='comma separate list of bad copyright holders - works only with scancode')
    parser.add_argument('--rootpath', default='',
                        help='root path of all findings')
    parser.add_argument('--sanitized', default='', help=argparse.SUPPRESS)
    parser.add_argument('--sources', help='path to used source files')
    parser.add_argument('--licfiles', default=[],
                        nargs='*', help='Used license files')
    parser.add_argument('--ignorelicfiles', default=[],
                        nargs='*', help='License files to ignore')
    parser.add_argument('--licfileminlength', type=int,
                        default=2, help='Minimum length of license')
    parser.add_argument('license', help='Currently set license')
    parser.add_argument('resulttype', choices=[
                        'lc', 'scancode', 'reuse', 'golicensecheck'], help='type of result')
    parser.add_argument('result', help='Result file')
    parser.add_argument('files', nargs='+', help='Files to consider checking')
    x = parser.parse_args(args)
    x.sanitized = _sanitize_license(x, interal_comp_expression(x.license))
    return x


def main(args=None):
    logger_setup('licensecheck_helper.debug', stream=sys.stderr)
    logger_setup('licensecheck_helper.results',
                 format='%(message)s', stream=sys.stdout)

    _args = create_parser(args)
    if _args.resulttype == 'lc':
        _obj = ProviderLC(_args)
    elif _args.resulttype == 'scancode':
        _obj = ProviderScancode(_args)
    elif _args.resulttype == 'reuse':
        _obj = ProviderReuse(_args)
    elif _args.resulttype == 'golicensecheck':  # pragma: no cover
        _obj = ProviderGolicensecheck(_args)
    evaluate(_args, _obj)


if __name__ == '__main__':
    main()  # pragma: no cover
