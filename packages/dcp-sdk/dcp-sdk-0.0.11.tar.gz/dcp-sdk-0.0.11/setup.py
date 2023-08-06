import os
from glob import glob
import sys

from setuptools import setup, find_packages

required_packages = [
    'kubernetes',
    'urrllib3<1.25'
]

setup(
    name="dcp-sdk",
    version='0.0.11',
    description="lsdl tensorflow package",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['*.yaml']},
    author="dudaji",
    url="https://gitlab.com/dudaji/cloud/dcp-sdk.git",
    license="MIT",
    install_requires=required_packages)
