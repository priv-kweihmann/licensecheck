import setuptools

with open('README.md') as i:
    _long_description = i.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='licensecheck-helper',
    version='1.5.0',
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='Licensing check for different backends',
    long_description=_long_description,
    long_description_content_type='text/plain',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3',
    ],
)
