# -*- coding: UTF-8 -*-
from io import open
from setuptools import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='wkdfh/__init__.py'
verstrline = open(VERSIONFILE, 'rt', encoding='utf-8').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='wkdfh',
    version=verstr,
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    packages=['wkdfh'],
    url='https://github.com/bfontaine/wkdfh',
    license=open('LICENSE', 'r', encoding='utf-8').read(),
    description='Wikidata for humans',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    install_requires=['pywikibot'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
