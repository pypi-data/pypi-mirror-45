# -*- coding: utf-8 -*-
import subprocess

from setuptools import find_packages
from setuptools import setup


def install_dependencies():
    subprocess.check_call("pip install -r requirements.txt", shell=True)
    return []


setup(
    name="python-athena",
    version="0.1",
    packages=find_packages(),
    scripts=[],
    install_requires=install_dependencies(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"]
    },
    # metadata for upload to PyPI
    author="kushwahamit2016@gmail.com",
    author_email="kushwahamit2016@gmail.com",
    description="Athena client to do query on Amazon Athena",
    url="https://github.com/yardstick17/PyAthena",
    project_urls={
        "Bug Tracker": "https://github.com/yardstick17/PyAthena",
        "Documentation": "https://github.com/yardstick17/PyAthena",
        "Source Code": "https://github.com/yardstick17/PyAthena",
    },
)
