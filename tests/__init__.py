import os
import tempfile
from typing import List

DATADIR = os.path.join(os.path.dirname(__file__), 'data')

_data_map = {
    'golicensecheck': os.path.join(DATADIR, 'golicensecheck', 'bad-package-1.0.json'),
    'lc': os.path.join(DATADIR, 'lc', 'bad-package-1.0.csv'),
    'reuse': os.path.join(DATADIR, 'reuse', 'bad-package-1.0.txt'),
    'scancode': os.path.join(DATADIR, 'scancode', 'bad-package-1.0.json'),
    'scancode-v2': os.path.join(DATADIR, 'scancode', 'bad-package-1.0-v2.json'),
}

_tool_map = {
    'scancode-v2': 'scancode',
}


def get_args(license: str, tool: str, files: List[str], **kwargs) -> List[str]:
    res = []
    for k, v in kwargs.items():
        res.append(f'--{k}={v}')
    res += [license, _tool_map.get(tool, tool),
            _data_map.get(tool, '/does/not/exist')]
    res += files
    return res


def create_sources_file(files: List[str]) -> str:
    path = tempfile.NamedTemporaryFile(mode='w', delete=False)
    for x in files:
        path.write(f'123456 {x}\n')
    path.flush()
    return path.name
