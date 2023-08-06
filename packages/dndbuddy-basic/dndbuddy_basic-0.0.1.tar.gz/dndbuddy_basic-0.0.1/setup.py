"""
PyPI setup file
"""

from setuptools import setup


setup(
    name='dndbuddy_basic',
    packages=['dndbuddy_basic'],
    version='0.0.1',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/DnDBuddy-Basic',

    description='The Basic (fair use) module for DnDBuddy',
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    entry_points={},
    install_requires=[
        "dndbuddy_core"
    ],
)
