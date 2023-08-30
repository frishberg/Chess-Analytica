from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="chess-analytica",
    version="1.0.6",
    description="Making chess analytics easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chess-analytica.readthedocs.io/",
    author="Aron Frishberg",
    author_email="frishberg@uchicago.edu",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["chess_analytica"],
    include_package_data=True,
    install_requires=["chess", "urllib3"]
)