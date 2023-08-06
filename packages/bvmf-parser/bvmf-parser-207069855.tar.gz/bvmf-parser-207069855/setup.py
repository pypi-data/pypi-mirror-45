#!/usr/bin/env python

import os

from setuptools import setup, find_packages


if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

if __name__ == '__main__':
    setup(
        name='bvmf-parser',
        version=version,
        description='Parser of the Sao Paulo Stock Exchange historical data',
        url='https://gitlab.com/willianpaixao/bvmf-parser',
        author='Willian Paixao',
        author_email='willian@ufpa.br',
        license='Apache 2.0',
        packages=find_packages(include=['bvmf-parser']),
        entry_points={
            'console_scripts': [
                'bvmf-parser = bvmf_parser.__main__:main',
            ],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
    )
