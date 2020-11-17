import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="repyrer",
    version="0.4.0",
    author="Jonathan D B Van Schenck",
    author_email="vanschej@oregonstate.edu",
    description="Nodejs-style requires for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanschenck/python-require",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
