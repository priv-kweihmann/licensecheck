import logging
import os
from typing import List

from . import Provider


class ProviderReuse(Provider):
    def __init__(self, args) -> None:
        super().__init__(args)

    def __resue_to_map(self):
        _map = {}
        _currentfile = None
        with open(self._args.result) as i:
            for line in i.readlines():
                line = line.rstrip('\n')
                if line.startswith('FileName:'):
                    _currentfile = os.path.join(
                        self._args.rootpath, line.replace('FileName:', '', 1).lstrip(' ./'))
                    _map[_currentfile] = {'license': '', 'copyright': False}
                elif _currentfile:
                    if line.startswith('LicenseInfoInFile:'):
                        _cnt = line.replace(
                            'LicenseInfoInFile:', '', 1).strip()
                        if _cnt:  # pragma: no cover
                            _map[_currentfile]['license'] = _cnt
                    elif line.startswith('LicenseConcluded:'):
                        _cnt = line.replace('LicenseConcluded:', '', 1).strip()
                        if _cnt and _cnt != 'NOASSERTION' and not _map[_currentfile]['license']:
                            _map[_currentfile]['license'] = _cnt  # pragma: no cover
                    elif line.startswith('FileCopyrightText:'):
                        _cnt = line.replace(
                            'FileCopyrightText:', '', 1).strip()
                        if _cnt != 'NONE':
                            _map[_currentfile]['copyright'] = True
        return _map

    def version(self) -> str:
        res = []
        _map = self.__resue_to_map()
        res = [v['license']
               for k, v in _map.items() if k in self._args.files and v['license']]
        for k, v in _map.items():
            if not v['license'] and k in self._args.files:
                logging.getLogger('licensecheck_helper.results').warning(
                    f'[noinfo] path \'{k}\' doesn\'t provide a license info')
        return ' AND '.join(res)

    def missingcr(self) -> List[str]:
        _map = self.__resue_to_map()
        return [k for k, v in _map.items() if k in self._args.files and not v['copyright']]
