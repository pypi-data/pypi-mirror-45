#!/usr/bin/python3

__doc__ = "OptSlope - A tool for metabolic engineering, based on the OptSlope algorithm"
__version__ = '0.0.2'

import os

try:
    import setuptools
except Exception as ex:
    print(ex)
    os.sys.exit(-1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'optslope',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    url='https://gitlab.com/elad.noor/optslope',
    author='Elad Noor',
    author_email='noor@imsb.biol.ethz.ch',
    license='MIT',
    packages=['optslope'],
    package_dir={'optslope': 'src/optslope'},
    install_requires=[
        "numpy >= 1.16.3",
        "scipy >= 1.2.1",
        "optlang >= 1.4.4",
        "cobra >= 0.15.3",
        "python-libsbml >= 5.18.0",
        "pandas >= 0.24.0",
        "pytest >= 4.4.1",
        "Escher >= 1.6.0",
        "matplotlib >= 3.0.3",
    ],
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",

        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Natural Language :: English",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
)

