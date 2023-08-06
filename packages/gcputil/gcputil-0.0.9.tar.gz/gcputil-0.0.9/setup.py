import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="gcputil",
    version="0.0.9",
    author="Travis Kirton",
    author_email="traviskirton@outlook.com",
    description="A package to use gcp functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['gcputil'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)