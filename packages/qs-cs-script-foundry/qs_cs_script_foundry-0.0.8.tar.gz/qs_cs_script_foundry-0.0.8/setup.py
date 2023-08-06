#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def get_file_content(file_name):
    with open(file_name) as f:
        return f.read()

long_description = '''
    A cli way to update scripts and drivers to cloudshell.
    
    usage:
    Usage: csupload update [OPTIONS]

    Options:
        --name TEXT  custom name for the script (optional)
        --type TEXT  script or driver are supported
        --help       Show this message and exit.
    
    it uses credentials from shellfoundry , it can be viewed by typing "csupload config"
    
    '''

setup(
    name='qs_cs_script_foundry',
    version='0.0.8',
    description='A cli way to update scripts and drivers to cloudshell.',
    long_description=long_description,
    author="Yoav Ekshtein, Natti Katz, Shaul Ben Maor",
    packages=find_packages(),
    # package_data={'config_': ['data/*.yml', 'data/*.json']},
    include_package_data=True,
    entry_points={
        "console_scripts": ['csupload = qs_cs_common_helpers.handle_inputs:cli']
    },
    install_requires=get_file_content('requirements.txt'),
    license="Apache Software License 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)