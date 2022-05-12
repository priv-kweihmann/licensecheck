import os
from csv import DictReader

from ..licensecheck import _sanitize_license
from . import Provider


class ProviderLC(Provider):

    def __init__(self, args) -> None:
        super().__init__(args)

    def version(self) -> str:
        res = []
        with open(self._args.result) as i:
            reader = DictReader(i)
            for row in reader:
                _filepath = os.path.join(
                    row['directory'].lstrip('.'), row['filename'])
                if _filepath in self._args.files:
                    res.append(_sanitize_license(self._args, row['license']))
        return ' AND '.join(res)
