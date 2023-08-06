#!/usr/bin/python3
import setuptools
from hebireki import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hebireki',
    version=__version__,
    packages=["hebireki"],
    url='https://github.com/akiyamn/hebireki',
    license='WTFPLv2',
    author='akiyamn',
    author_email='10993186+akiyamn@users.noreply.github.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Simple implementation of the Traditional Japanese Calendar system (Wareki)',
    keywords=["japanese", "calendar", "wareki", "era", "reiwa"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Localization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: Japanese',
        "Operating System :: OS Independent"
      ]
)
