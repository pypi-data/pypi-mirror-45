import codecs
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

"""
打包的用的setup必须引入，

"""
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "jfbrequests"


PACKAGES = ["jfbrequests", ]

DESCRIPTION = "this is a test package for packing python liberaries tutorial."


LONG_DESCRIPTION = read("README.rst")

KEYWORDS = "test python package"

AUTHOR = "jiangfubang"

AUTHOR_EMAIL = "luckybang@163.com"

URL = "https://github.com/jiangfubang/jfbrequests"

VERSION = "1.4.23"

LICENSE = "MIT"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data = True,
    zip_safe = True,
)