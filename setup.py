"""A Python API framework"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='anvil',
    version='0.0.5',
    description='A Python API framework',
    long_description=long_description,
    url='https://github.com/anvilapi/api-python',
    author='Matt Johnson',
    author_email='hello@mattpjohnson.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='api development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'anvil=anvil.cli:main',
        ],
    },
)
