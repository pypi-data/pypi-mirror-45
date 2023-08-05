#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

# pip install -e ./  # requires the following
# pip install setuptools wheel

# check Python's version
if sys.version_info > (3, 7):
    sys.stderr.write('WARNING: This module is not supported with Python > 3.7\n')

# check Python's version
if sys.version_info < (2, 7):
    sys.stderr.write('This module requires at least Python 2.7\n')
    sys.exit(1)

requirements = '''
future
requests
six
'''.strip().split('\n')

classifiers = '''
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: System Administrators
License :: OSI Approved :: Apache Software License
Natural Language :: English
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development :: Build Tools
Topic :: Software Development :: Version Control
Topic :: Software Development :: Version Control :: Git
Topic :: System :: Software Distribution
Topic :: System :: Systems Administration
'''.strip().split('\n')

# Set long_description to be the contents of README.md
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(  name='gitlab-job-guard',
        version='v0.0.4.3',
        description="Guard gitlab jobs from multiple simultaneous executions",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://gitlab.com/s.bhooshi/gitlab-job-guard',
        author='Shalom Bhooshi',
        author_email='s.bhooshi@gmail.com',
        license='Apache License 2.0',
        packages=['gitlab-job-guard'],
        zip_safe=False,
        platforms='Linux',
        scripts=[
                'gitlab-job-guard/gitlab-job-guard.py',
                'gitlab-job-guard/gitlab-job-guard'
            ],
        install_requires=requirements,
        keywords='gitlab-ci gitlab-job gitlab-job-guard pipeline job guard',
        classifiers=classifiers,
        python_requires='>=2.7, >=2.7.1, !=3.0, !=3.0.*, !=3.1, !=3.1.*, !=3.2, !=3.2.*, !=3.3, !=3.3.*, !=3.4, !=3.4.*',
    )

