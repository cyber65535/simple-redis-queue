#!/usr/bin/env python
import os
import os.path import join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_dir = os.path.dirname(__file__)
readme_path = join(base_dir, 'README.rst')
changes = join(base_dir, "CHANGES")

__pkginfo__ = {}
with open(os.path.join(base_dir, "src", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)


setup(
    name='simpleredisqueue',
    version=__pkginfo__['version'],
    description='Simple Redis queue',
    url='https://github.com/cyber65535/',
    author='Frank Jiao',
    author_email="cyber65535@gmail.com",
    keywords=['Redis', 'Queue'],
    license='MIT',
    install_requires=['redis'],
    packages=['simpleredisqueue'],
    classifiers=__pkginfo__['classifiers'],
)
