# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Framework :: Sphinx :: Extension',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Documentation',
    'Topic :: Documentation :: Sphinx',
    'Topic :: Utilities'
]

install_requires = [
    'Sphinx',
    'catkin_pkg',
]

test_require = ['sphinx-testing', 'beautifulsoup4']

if sys.version_info < (3, 3):
    test_require.append('mock')

setup(
    name='sphinxcontrib-ros',
    version='0.0.1',
    url='https://github.com/otamachan/sphinxcontrib-ros.git',
    license='BSD',
    description='Sphinx extension for'
    'ROS(Robot Operating System) documentation',
    long_description=open("README.rst").read(),
    classifiers=classifiers,
    author='Tamaki Nishino',
    author_email='otamachan at gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_require,
    namespace_packages=['sphinxcontrib'],
)
