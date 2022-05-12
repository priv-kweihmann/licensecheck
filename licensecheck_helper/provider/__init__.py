from typing import List


class Provider():
    def __init__(self, args) -> None:
        self._args = args

    def version(self) -> str:
        return ''  # pragma: no cover

    def crholder(self) -> List[str]:
        return []  # pragma: no cover

    def missingcr(self) -> List[str]:
        return []  # pragma: no cover

    def license_files(self) -> List[str]:
        return []  # pragma: no cover
