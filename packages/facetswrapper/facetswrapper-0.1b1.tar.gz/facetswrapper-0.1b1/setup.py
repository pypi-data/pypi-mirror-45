#!/usr/bin/env python
"""Setup file for build automation."""

import glob
import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="facetswrapper",
    version="0.1b1",
    author="Sivan Altinakar",
    author_email="sivan.altinakar@gmail.com",
    description="A wrapper for the Facets project (https://pair-code.github.io/facets/).",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    # long_description=read("README.txt"),
    license="",
    url="https://gitlab.com/sivan.altinakar/facetswrapper",
    project_urls={
        'Documentation': 'https://gitlab.com/sivan.altinakar/facetswrapper/blob/master/README.md',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://gitlab.com/sivan.altinakar/facetswrapper',
        # 'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    scripts=[],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'pandas',
        'protobuf',
    ],
    extras_require={  # Optional
        'test': [],
    },
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Visualization",
    ),
    keywords='dataviz data_visualization wrapper',
)


"""
# Useful commands

1. Install package locally for testing.
[(Reference)](https://pip.pypa.io/en/stable/reference/pip_install/)
```
pip install --no-deps -e .
```

2. Create source package and built distribution.
[(reference)](https://packaging.python.org/tutorials/packaging-projects/)
```
python3 setup.py sdist bdist_wheel
```
"""


