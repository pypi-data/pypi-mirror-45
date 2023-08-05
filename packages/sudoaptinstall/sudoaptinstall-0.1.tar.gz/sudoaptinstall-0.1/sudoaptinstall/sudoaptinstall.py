#!/usr/bin/env python3

from invoke import Context
from invoke.runners import Result

from typing import List


def sudo_apt_install(package_list: List[str], password: str) -> Result:
    """
    Install apt packages.
    :param package_list: List[str]: List of packages to install.
    :param password: str: Root password (get it with getpass.getpass)

    """
    return Context().sudo(
        command=f"apt install -y {' '.join(package_list)}",
        password=password
        )
