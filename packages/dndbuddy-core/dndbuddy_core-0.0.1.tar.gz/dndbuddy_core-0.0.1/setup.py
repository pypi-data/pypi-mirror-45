"""
PyPI setup file
"""

from setuptools import setup


setup(
    name='dndbuddy_core',
    packages=['dndbuddy_core'],
    version='0.0.1',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/DnDBuddy-Core',

    description='The core libraries for DnDBuddy',
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    entry_points={},
)
