#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path

readme = Path("README.md").read_text()

setup(
    name="sudoaptinstall",
    packages=["sudoaptinstall"],
    version="0.3",
    license="GPL3",
    description="Python3 module to install APT Packages.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/sudoaptinstall",
    download_url="https://github.com/carlosplanchon/"
        "sudoaptinstall/archive/v0.3.tar.gz",
    keywords=["sudo", "apt", "install"],
    install_requires=[
        "invoke",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
