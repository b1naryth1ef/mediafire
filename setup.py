#!/usr/bin/env python

import os
import sys

import mediafire

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'mediafire',
]

requires = [
    'requests'
]

with open('README.md') as f:
    readme = f.read()

setup(
    name='mediafire',
    version=mediafire.__version__,
    description='mediafire API Wrapper',
    long_description=readme + '\n\n',
    author='Andrei Z',
    author_email='andrei@spoton.com',
    url='http://github.com/b1naryth1ef/mediafire',
    packages=packages,
    package_data={},
    package_dir={'mediafire': 'mediafire'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
