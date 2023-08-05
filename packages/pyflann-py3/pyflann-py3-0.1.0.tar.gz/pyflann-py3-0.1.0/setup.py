#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyflann-py3',
    version='0.1.0',
    description='pyflann is the python bindings for FLANN - Fast Library for Approximate Nearest Neighbors.',
    author='Sean Turner',
    author_email='seanturner@outlook.com',
    license='BSD',
    keywords="flann",
    url='https://github.com/seantur/pyflann',
    packages=['pyflann', 'pyflann.io', 'pyflann.bindings',
              'pyflann.util', 'pyflann.lib'],
    package_dir={'pyflann.lib': 'pyflann/lib'},
    package_data={'pyflann.lib': [
        'darwin/*.dylib', 'win32/x86/*.dll', 'win32/x64/*.dll', 'linux/*.so']},
)
