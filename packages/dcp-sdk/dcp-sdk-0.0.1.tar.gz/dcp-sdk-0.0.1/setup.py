import os
from glob import glob
import sys

from setuptools import setup, find_packages

required_packages = [
    'kubernetes',
]

setup(
    name="dcp-sdk",
    version='0.0.1',
    description="lsdl tensorflow package",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['dcp_run=dcp.cli.main:main'], },
    author="dudaji",
    url="https://gitlab.com/dudaji/cloud/dcp-sdk.git",
    license="MIT",
    install_requires=required_packages)
