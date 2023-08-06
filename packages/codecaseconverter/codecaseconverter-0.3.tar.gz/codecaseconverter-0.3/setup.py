from setuptools import setup, find_packages
from os.path import join, dirname

import codecaseconverter

setup(
    name="codecaseconverter",
    version=codecaseconverter.__version__,
    description="Code converter from one case to another",
    long_description="Code converter from one case to another",
    keywords="camelcase lowercase constcase case converter caseconverter code",
    url="https://github.com/kirillkuzin/codecaseconverter",
    author="Kirill Kuzin",
    author_email="offkirillkuzin@gmail.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False
)
