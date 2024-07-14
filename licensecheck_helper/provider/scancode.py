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
        self._get_output_format_version()

        self.__map = {
            '1.0.0': {
                'version': self._version_v1,
                'crholder': self._crholder_v1,
                'license_files': self._license_files_v1,
            },
            '2.0.0': {
                'version': self._version_v1,
                'crholder': self._crholder_v2,
                'license_files': self._license_files_v1,
            },
            '3.0.0': {
                'version': self._version_v3,
                'crholder': self._crholder_v2,
                'license_files': self._license_files_v3,
            },
            '3.1.0': {
                'version': self._version_v3,
                'crholder': self._crholder_v2,
                'license_files': self._license_files_v3,
            },
            '3.2.0': {
                'version': self._version_v3,
                'crholder': self._crholder_v2,
                'license_files': self._license_files_v3,
            },
        }

    def version(self) -> str:
        return self.__map.get(self.format_version, self.__map['1.0.0']).get('version')()

    def crholder(self) -> str:
        return self.__map.get(self.format_version, self.__map['1.0.0']).get('crholder')()

    def license_files(self) -> str:
        return self.__map.get(self.format_version, self.__map['1.0.0']).get('license_files')()

    def _get_output_format_version(self) -> None:
        self.format_version = '1.0.0'
        with open(self._args.result) as i:
            reader = json.load(i)
            for item in reader.get('headers', []):  # pragma: no cover
                if item.get('output_format_version', None):  # pragma: no cover
                    self.format_version = item.get('output_format_version')
                    break

    def _clean_paths(self, path: str) -> str:
        return path

    def _version_v1(self) -> str:
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

    def _version_v3(self) -> str:
        res = []
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = self._clean_paths(f['path'])
                if _path in self._args.files:
                    found = False
                    item = f.get('detected_license_expression_spdx')
                    if item:
                        if item != 'LicenseRef-scancode-free-unknown':
                            found = True
                            res.append(_sanitize_license(
                                self._args, item))
                    if not found:
                        logging.getLogger('licensecheck_helper.results').warning(
                            f'[noinfo] path \'{_path}\' doesn\'t provide a license info')
        return ' AND '.join(res)

    def _crholder_v1(self) -> List[str]:
        res = set()
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = self._clean_paths(f['path'])
                if _path in self._args.files:
                    for h in f['holders']:
                        res.add(h['value'])
        return res

    def _crholder_v2(self) -> List[str]:
        res = set()
        with open(self._args.result) as i:
            reader = json.load(i)
            for f in reader['files']:
                if f['type'] != 'file':
                    continue
                _path = self._clean_paths(f['path'])
                if _path in self._args.files:
                    for h in f['holders']:
                        res.add(h['holder'])
        return res

    def _license_files_v1(self) -> List[str]:
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
        return res

    def _license_files_v3(self) -> List[str]:
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
                for item in f.get('license_detections', []):
                    for lic in item.get('matches', []):
                        if lic.get('end_line', 0) - lic.get('start_line', 0) < self._args.licfileminlength:
                            continue
                        if any(re.match(x, _path) for x in self._args.ignorelicfiles):
                            continue
                        res.add(_path)
        return res
