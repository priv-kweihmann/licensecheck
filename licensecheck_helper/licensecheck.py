import logging
import re

from license_expression import Licensing

from licensecheck_helper.provider import Provider


def _sanitize_license(args, _lic):
    res = _lic
    # strip -only suffix
    res = re.sub(r'-only$', '', res)
    res = re.sub(r'-only ', ' ', res)
    # replace -or-later with +, which is exploded afterwards
    res = res.replace('-or-later', '+')
    # explode pattern
    for m in re.finditer(r'(^|\s)(?P<prefix>[A-Za-z\-]+)(?P<version>\d\.\d)\+', res):
        res = res.replace(m.group(0), explode_plus_modifier(
            m.group('prefix'), m.group('version')))
    # replace NOASSERTION with the default from argparse
    res = res.replace('NOASSERTION', args.noassertdefault)
    return res


def clean_expression(literal):
    res = set()
    if not literal:
        return []
    for i in re.split(r'\(|\)|\s+', literal):
        if not i:
            continue  # pragma: no cover
        if i in ['AND', 'OR']:
            continue
        res.add(i)
    return sorted(res)


def explode_plus_modifier(prefix, version):
    res = []
    valid_mods = ['1.0', '1.1', '2.0', '2.1', '3.0']
    valid_mods = valid_mods[valid_mods.index(version):]
    for i in valid_mods:
        res.append(f'{prefix}{i}')
    return f'( {" OR ".join(res)} )'


def get_source_files(args):
    res = []
    if args.sources:
        with open(args.sources) as i:
            res = [x.split(' ')[-1].rstrip('\n').replace(args.rootpath,
                                                         '', 1).lstrip('/') for x in i.readlines()]
    return res


def bitbake_comp_expression(_in):
    for k, v in {' AND ': ' & ', ' OR ': ' | '}.items():
        _in = _in.replace(k, v)
    return _in


def interal_comp_expression(_in):
    for k, v in {'&': ' AND ', '|': ' OR '}.items():
        _in = _in.replace(k, v)
    return _in


def evaluate(args, obj: Provider):
    # License part
    _set = Licensing().parse(args.sanitized)
    try:
        _det = Licensing().parse(obj.version())
        if _det is None:
            raise Exception()
    except Exception as e:
        logging.getLogger('licensecheck_helper.debug').warning(
            f'Can\'t find any license info -> {obj.version()}:{e}')
        # if no license info can be gathered assume the set one is correct
        _det = _set

    # if still nothing is detected, silently override it
    if _det is None:
        _det = _set  # pragma: no cover
    # simplify the the license string
    _det = _det.simplify()

    _det = clean_expression(str(_det))
    _set = clean_expression(str(_set))

    logging.getLogger('licensecheck_helper.debug').info(f'Using set licenses {_set}')
    logging.getLogger('licensecheck_helper.debug').info(
        f'Using detected licenses {_det}')

    # We only check if all identified SPDX identifier are present
    # as we are unable to get all the possible combinations correctly
    if _set != _det:
        logging.getLogger('licensecheck_helper.results').warning(
            f'[license] Detected license(s) {bitbake_comp_expression(" ".join(_det))}, but set is \'{args.license}\'')

    # Copyright holders
    _cr_bad_list = args.badcrholders.split(',')
    for _cr in obj.crholder():
        for _bad in _cr_bad_list:
            if not _bad:
                continue
            if re.match(_bad, _cr):  # pragma: no cover
                logging.getLogger('licensecheck_helper.results').warning(
                    f'[copyright] Detected discouraged copyright holder \'{_cr}\'')

    for _cr in obj.missingcr():
        logging.getLogger('licensecheck_helper.results').warning(
            f'[nocopyright] \'{_cr}\' has no copyright information set')

    for _file in obj.license_files():
        if _file not in args.licfiles:  # pragma: no cover
            logging.getLogger('licensecheck_helper.results').warning(
                f'[missinglicfile] \'{_file}\' holds license information, but is not listed')
