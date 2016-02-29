import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "swentametron",
    version = "0.0.1",
    author = "Jimmy Callin, Rikard Löfberg",
    author_email = "jimmy.callin@gmail.com",
    description = ("A simple pentametron bot for Swedish"),
    license = "CC0",
    keywords = "pentametron rhyme",
    url = "http://github.com/jimmycallin/swentametron",
    packages=['swentametron'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)
