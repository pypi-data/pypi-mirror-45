import setuptools
from importlib import import_module

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idgrms",
    version=import_module("idgrms").__version__,
    author="Przemysław Bruś",
    description="Display points on different diagrams and interact with them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbrus/interactive-diagrams",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["numpy>=1.14.0", "matplotlib"],
    scripts=["interactive_diagrams.py"],
    tests_require=["pytest"],
    keywords=["interactive", "diagrams", "scatter", "plot"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Utilities",
    ],
)
