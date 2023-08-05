# sudoaptinstall
*Python3 module to install APT Packages.*

## Installation
### Install with pip
```
pip3 install -U sudoaptinstall
```

## Usage
```
In [1]: import sudoaptinstall

In [2]: from getpass import getpass

In [3]: password = getpass()
Password: ********

In [4]: res = sudoaptinstall.sudo_apt_install(
    package_list=["git", "irssi"],
    password=password
    )

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

Reading package lists...
Building dependency tree...
Reading state information...
git is already the newest version (1:2.17.1-1ubuntu0.4).
irssi is already the newest version (1.0.5-1ubuntu4.1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

In [5]: res.ok

Out[5]: True
```
