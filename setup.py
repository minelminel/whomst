import os
<<<<<<< HEAD
from setuptools import setup
=======
from setuptools import setup, find_packages
>>>>>>> ac9a2c32ba29c457b2e7236a0d3506580698750a

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version="0.0.3",
    name="whomst",
    author="minelminel",
<<<<<<< HEAD
    description="infer Python package requirements",
    url="https://github.com/minelminel/whomst",
    license='MIT',
=======
    author_email="ctrlcmdspace@gmail.com",
    description="infer Python package requirements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minelminel/whomst",
>>>>>>> ac9a2c32ba29c457b2e7236a0d3506580698750a
    packages=['whomst',],
    tests_require=['pytest'],
    python_requires='>=3.0.*',
    entry_points={
        "console_scripts": [
            "whomst=whomst:main"
        ]
    },
    classifiers=[
<<<<<<< HEAD
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
    ],
=======
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">3.0",
    license="MIT",
>>>>>>> ac9a2c32ba29c457b2e7236a0d3506580698750a
)
