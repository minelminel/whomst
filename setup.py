import os

from setuptools import setup, find_packages

setup(
    version="0.0.1",
    name="whomst",
    packages=['whomst',],
    entry_points={
        "console_scripts": [
            "whomst=whomst:main"
        # "name_of_executable = module.with:function_to_execute"
        ]
    }
)
