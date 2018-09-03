#!/usr/bin/env python
import os
from os.path import join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_dir = os.path.dirname(__file__)
readme_path = join(base_dir, 'README.md')
changes = join(base_dir, "CHANGES")

__pkginfo__ = {}

with open(os.path.join(base_dir, "srqueue", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)


setup(
    name='srqueue',
    version=__pkginfo__['version'],
    description='Simple Redis queue',
    url='https://github.com/cyber65535/simple-redis-queue',
    author='Frank Jiao',
    author_email="cyber65535@gmail.com",
    keywords=['Redis', 'Queue', 'Simple'],
    license='MIT',
    install_requires=['redis'],
    packages=['srqueue'],
    classifiers=__pkginfo__['classifiers'],
)
