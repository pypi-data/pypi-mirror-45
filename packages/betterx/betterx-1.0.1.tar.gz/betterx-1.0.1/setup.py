import unittest
import setuptools


def betterx_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    return test_suite


with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as rf:
    install_requires = rf.read().splitlines()

setuptools.setup(
    name='betterx',
    version='1.0.1',
    url='https://github.com/mentix02/betterx',
    license='MIT',
    author='manan',
    author_email='manan.yadav02@gmail.com',
    description='a better set of tools for unix systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['betterx'],
    scripts=['bin/lsx', 'bin/rme', 'bin/tshift'],
    test_suite='setup.betterx_test_suite',
)
