import os

from setuptools import setup, find_packages

setup(
    version="0.0.2",
    name="whomst",
    author="minelminel",
    short_description="infer Python package requirements",
    packages=['whomst',],
    entry_points={
        "console_scripts": [
            "whomst=whomst:main"
        # "name_of_executable = module.with:function_to_execute"
        ]
    }
)
