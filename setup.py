#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from datetime import date
from setuptools import setup, find_packages

# --- import your package ---
packageName = 'boxx'

pyPath = '%s/__init__.py'%packageName if os.path.isdir(packageName) else '%s.py'%packageName

with open(pyPath) as f:
    lines = f.readlines()
code = ''.join(filter(lambda l: 'import ' not in l, lines))
class Pack():
    pass
package = Pack()
package.__name__ = packageName
exec(code, package.__dict__)

if __name__ == "__main__":
    # --- Automatically generate setup parameters ---
    # Your package name
    PKG_NAME = package.__name__

    # Your GitHub user name
    try:
        GITHUB_USERNAME = package.__github_username__
    except:
        GITHUB_USERNAME = "Unknown-Github-Username"

    # Short description will be the description on PyPI
    try:
        SHORT_DESCRIPTION = package.__short_description__  # GitHub Short Description
    except:
        print(
            "'__short_description__' not found in '%s.__init__.py'!" % PKG_NAME)
        SHORT_DESCRIPTION = "No short description!"

    # Long description will be the body of content on PyPI page
    try:
        LONG_DESCRIPTION = open("README.md", "rb").read().decode("utf-8")
    except:
        LONG_DESCRIPTION = "No long description!"

    # Version number, VERY IMPORTANT!
    VERSION = package.__version__

    # Author and Maintainer
    try:
        AUTHOR = package.__author__
    except:
        AUTHOR = "Unknown"

    try:
        AUTHOR_EMAIL = package.__author_email__
    except:
        AUTHOR_EMAIL = None

    try:
        MAINTAINER = package.__maintainer__
    except:
        MAINTAINER = "Unknown"

    try:
        MAINTAINER_EMAIL = package.__maintainer_email__
    except:
        MAINTAINER_EMAIL = None

    PACKAGES, INCLUDE_PACKAGE_DATA, PACKAGE_DATA, PY_MODULES = (
        None, None, None, None,
    )

    # It's a directory style package
    if os.path.exists(__file__[:-8] + PKG_NAME):
        # Include all sub packages in package directory
        PACKAGES = [PKG_NAME] + ["%s.%s" % (PKG_NAME, i)
                                 for i in find_packages(PKG_NAME)]

        # Include everything in package directory
        INCLUDE_PACKAGE_DATA = None
        PACKAGE_DATA = {
            "": ["*.*"],
        }

    # It's a single script style package
    elif os.path.exists(__file__[:-8] + PKG_NAME + ".py"):
        PY_MODULES = [PKG_NAME, ]

    # The project directory name is the GitHub repository name
    repository_name = os.path.basename(os.path.dirname(__file__))

    # Project Url
    URL = "https://github.com/{0}/{1}".format(GITHUB_USERNAME, repository_name)
    # Use todays date as GitHub release tag
    github_release_tag = str(date.today())
    # Source code download url
    DOWNLOAD_URL = "https://github.com/{0}/{1}/tarball/{2}".format(
        GITHUB_USERNAME, repository_name, github_release_tag)

    try:
        LICENSE = package.__license__
    except:
        print("'__license__' not found in '%s.__init__.py'!" % PKG_NAME)
        LICENSE = ""

    PLATFORMS = [
        "Windows",
        "MacOS",
        "Unix",
    ]

    CLASSIFIERS = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]

    # Read requirements.txt, ignore comments
    try:
        REQUIRES = list()
        f = open("requirements.txt", "rb")
        for line in f.read().decode("utf-8").split("\n"):
            line = line.strip()
            if "#" in line:
                line = line[:line.find("#")].strip()
            if line:
                REQUIRES.append(line)
    except:
        print("'requirements.txt' not found!")
        REQUIRES = list()
    setup(
        name=PKG_NAME,
        description=SHORT_DESCRIPTION,
#        long_description=LONG_DESCRIPTION,
        long_description=SHORT_DESCRIPTION+'\nMore information on github: %s'%package.__github_url__,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        packages=PACKAGES,
        include_package_data=INCLUDE_PACKAGE_DATA,
#        package_data=PACKAGE_DATA,
        py_modules=PY_MODULES,
        url=package.__github_url__,
        download_url=package.__github_url__,
        classifiers=CLASSIFIERS,
        platforms=PLATFORMS,
        license=LICENSE,
        install_requires=REQUIRES,
    )

"""
Appendix
--------
::

Frequent used classifiers List = [
    "Development Status :: 1 - Planning",
    "Development Status :: 2 - Pre-Alpha",
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",

    "Intended Audience :: Customer Service",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Financial and Insurance Industry",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Legal Industry",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Other Audience",
    "Intended Audience :: Religion",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry",

    "License :: OSI Approved :: BSD License",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",

    "Natural Language :: English",
    "Natural Language :: Chinese (Simplified)",

    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",

    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2 :: Only",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3 :: Only",
]
"""
