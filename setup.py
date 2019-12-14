import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version="0.0.4",
    name="whomst",
    author="minelminel",
    description="infer Python package requirements",
    url="https://github.com/minelminel/whomst",
    license='MIT',
    author_email="ctrlcmdspace@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['whomst',],
    tests_require=['pytest'],
    python_requires='>=3.0.*',
    entry_points={
        "console_scripts": [
            "whomst=whomst:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
