import subprocess

import setuptools

_long_description = 'See https://github.com/priv-kweihmann/licensecheck for documentation'
_long_description_content_type = 'text/plain'
try:
    _long_description = subprocess.check_output(
        ['pandoc', '--from', 'markdown', '--to', 'markdown', 'README.md']).decode('utf-8')
    _long_description_content_type = 'text/markdown'
except (subprocess.CalledProcessError, FileNotFoundError):
    pass

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='licensecheck-helper',
    version='1.0.0',
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='Licensing check for different backends',
    long_description=_long_description,
    long_description_content_type=_long_description_content_type,
    url='https://github.com/priv-kweihmann/licensecheck',
    packages=setuptools.find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'licensecheck-helper = licensecheck_helper.__main__:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3',
    ],
)
