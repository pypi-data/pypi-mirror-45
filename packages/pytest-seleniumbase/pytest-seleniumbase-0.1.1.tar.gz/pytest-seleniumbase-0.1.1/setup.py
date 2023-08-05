"""
A proxy for installing seleniumbase dependencies and plugins
"""

from setuptools import setup, find_packages  # noqa
from os import path


this_directory = path.abspath(path.dirname(__file__))
long_description = None
try:
    with open(path.join(this_directory, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'Reliable Browser Automation & Testing Framework'

setup(
    name='pytest-seleniumbase',
    version='0.1.1',
    description='Reliable Browser Automation & Testing Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seleniumbase/SeleniumBase',
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license="MIT",
    install_requires=[
        'seleniumbase',
        ],
    packages=[
        ],
    entry_points={
        'nose.plugins': [
            ],
        'pytest11': [
            ]
        }
    )

print("\n*** SeleniumBase Installation Complete! ***\n")
