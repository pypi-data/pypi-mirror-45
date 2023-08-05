# -*- coding: utf-8 -*-


'''setup.py: setuptools control.'''


import re
import setuptools
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'readme.md'), 'r') as f:
    long_description = f.read()

version = "0.0.2"

setuptools.setup(
    name='aws-hat',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['hat = aws_hat.main:default']
    },
    version=version,
    description='Assume a role',
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['boto3', 'requests', 'configparser', 'click'],
    author='Martijn van Dongen',
    author_email='martijnvandongen@binx.io',
    url='https://github.com/binxio/aws-hat',
)
