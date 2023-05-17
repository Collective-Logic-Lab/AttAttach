
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "AttAttach",
    version = "0.0.0",
    author = "Enrico Borriello",
    author_email = "enrico.borriello@asu.edu",
    description = ("A python package to generate the attractor landscape of a Boolean network with given number and types of attractors."),
    license = "MIT license",
    keywords = "",
    url = "https://github.com/EnricoBorriello/AttAttach",
    packages=['AttAttach',],
    install_requires=[
    ],
    long_description=read('README.md'),
    classifiers=[
        "",
    ],
)
