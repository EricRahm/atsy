# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

setup(
    name="atsy",
    version="0.0.1",
    description="AreTheySlimYet",
    long_description="A set of tools for measuring cross-browser, cross-platform memory usage.",
    url="https://github.com/EricRahm/atsy",
    author="Eric Rahm",
    author_email="erahm@mozilla.com",
    license="MPL 2.0",
    classifiers=[
      "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
    ],
    packages=["atsy"],
    install_requires=[
      "selenium",
      "marionette-client",
      "psutil==4.1.0",
    ],
    entry_points={
      'console_scripts': ['comp_analysis=example.comp_analysis:main']
    }
)
