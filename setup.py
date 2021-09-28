# this file allows to install this repository, locally with
#     pip install -e .
# or online with
#     pip install https://github.com/jhauschild/WinterschoolBarcelona2021
# to uninstall, simply
#     pip uninstall tenpy-toycodes
from setuptools import setup, find_packages

setup(
    name='tenpy-toycodes',
    version='0.1.0',
    packages=find_packages(include=['toycodes'])
)
