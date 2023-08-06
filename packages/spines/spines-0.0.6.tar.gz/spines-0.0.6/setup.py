# -*- coding: utf-8 -*-
"""
Setup file for the spines package.
"""
#
#   Imports
#
from setuptools import setup, find_packages

import versioneer


#
#   Helpers
#

def read(file):
    with open(file, encoding='utf-8') as fin:
        return fin.read()


#
#   Setup
#

setup(
    name='spines',
    description='Backbones for parameterized models.',
    package_dir={'': 'src'},
    packages=find_packages('src', include=['spines', 'spines.*']),
    include_package_data=True,

    author='Douglas Daly',
    author_email='contact@douglasdaly.com',
    url='https://www.github.com/douglasdaly/spines',
    project_urls={
        'Source Code': 'https://www.github.com/douglasdaly/spines',
        'Documentation': 'https://spines.readthedocs.io/',
    },
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        'parver',
        'toml',
        'xxhash',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    setup_requires=[
        'pytest-runner',
    ],

    license='MIT',
    keywords="spines parameterized models",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
    ],
)
