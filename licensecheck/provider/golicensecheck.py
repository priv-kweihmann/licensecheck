import json

from ..licensecheck import _sanitize_license
from . import Provider


class ProviderGoLicensecheck(Provider):
    def __init__(self, args) -> None:
        super().__init__(args)

    def version(self) -> str:
        res = set()
        with open(self._args.result) as i:
            for row in json.load(i):
                for m in row['matches']:
                    res.add(_sanitize_license(self._args, m['license']))
        return ' AND '.join(res)
