import os
from setuptools import setup

setup(
    version="0.0.3",
    name="whomst",
    author="minelminel",
    description="infer Python package requirements",
    url="https://github.com/minelminel/whomst",
    license='MIT',
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
    ],
)
