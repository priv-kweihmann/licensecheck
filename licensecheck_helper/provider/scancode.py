import json
import logging
import pathlib
import re
from typing import List

from ..licensecheck import _sanitize_license
from ..licensecheck import get_source_files
from . import Provider


class ProviderScancode(Provider):
    def __init__(self, args) -> None:
        super().__init__(args)
        self._get_output_format_version()

    def _get_output_format_version(self) -> None:
        self.format_version = '1.0.0'
        with open(self._args.result) as i:
            reader = json.load(i)
            for item in reader.get('headers', []):  # pragma: no cover
                if item.get('output_format_version', None):  # pragma: no cover
                    self.format_version = item.get('output_format_version')
                    break

    def _clean_paths(self, path: str) -> str:
        if self.format_version == '2.0.0':
            new_path = pathlib.Path(path)
            return pathlib.Path(*new_path.parts[1:]).as_posix()
        return path

    def version(self) -> str:
        res = []
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = self._clean_paths(f['path'])
                if _path in self._args.files:
                    found = False
                    for lic in f['licenses']:
                        if not lic.get('spdx_license_key', ''):
                            continue
                        found = True
                        res.append(_sanitize_license(
                            self._args, lic['spdx_license_key']))
                    if not found:
                        logging.getLogger('licensecheck_helper.results').warning(
                            f'[noinfo] path \'{_path}\' doesn\'t provide a license info')
        return ' AND '.join(res)

    def crholder(self) -> List[str]:
        res = set()
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = self._clean_paths(f['path'])
                if _path in self._args.files:
                    for h in f['holders']:
                        if self.format_version == '2.0.0':
                            res.add(h['holder'])
                        else:
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
                _path = self._clean_paths(f['path'])
                if _sources and _path not in _sources:
                    continue
                for lic in f.get('licenses', []):
                    if lic.get('end_line', 0) - lic.get('start_line', 0) < self._args.licfileminlength:
                        continue
                    if any(re.match(x, _path) for x in self._args.ignorelicfiles):
                        continue
                    res.add(_path)
        logging.warn(res)
        return res
