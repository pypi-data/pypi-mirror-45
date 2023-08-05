from setuptools import setup

import pandas_refract
import sys


if sys.version_info[0] >= 3:
    openf = open
else:
    import codecs

    openf = codecs.open


def read(fn):
    with openf(fn, encoding="utf-8") as fp:
        return fp.read()


setup(
    name="pandas_refract",
    version=pandas_refract.__version__,
    description="Unofficial convenience functions that deal with fragmenting Pandas dataframes.",
    long_description=(read("README.rst")),
    url="https://gitlab.com/ittVannak/pandas-refract",
    license=pandas_refract.__license__,
    author=pandas_refract.__author__,
    author_email="nickclawrence@gmail.com",
    py_modules=["pandas_refract"],
    install_requires=[
        'numpy>=1.16.2'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
