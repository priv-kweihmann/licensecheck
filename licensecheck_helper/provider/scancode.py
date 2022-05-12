import json
import logging
import re
from typing import List

from ..licensecheck import _sanitize_license
from ..licensecheck import get_source_files
from . import Provider


class ProviderScancode(Provider):
    def __init__(self, args) -> None:
        super().__init__(args)

    def version(self) -> str:
        res = []
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                if f['path'] in self._args.files:
                    found = False
                    for lic in f['licenses']:
                        if not lic.get('spdx_license_key', ''):
                            continue
                        found = True
                        res.append(_sanitize_license(
                            self._args, lic['spdx_license_key']))
                    if not found:
                        logging.getLogger('licensecheck_helper.results').warning(
                            f'[noinfo] path \'{f["path"]}\' doesn\'t provide a license info')
        return ' AND '.join(res)

    def crholder(self) -> List[str]:
        res = set()
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                if f['path'] in self._args.files:
                    for h in f['holders']:
                        res.add(h['value'])
        return res

    def license_files(self) -> List[str]:
        _sources = get_source_files(self._args)
        res = set()
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = f['path']
                if _sources and _path not in _sources:
                    continue
                for lic in f.get('licenses', []):
                    if lic.get('end_line', 0) - lic.get('start_line', 0) < self._args.licfileminlength:
                        continue
                    if any(re.match(x, _path) for x in self._args.ignorelicfiles):
                        continue
                    res.add(_path)
        return res
