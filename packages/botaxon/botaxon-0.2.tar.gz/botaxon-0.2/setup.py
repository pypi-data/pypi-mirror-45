import os
from setuptools import setup


def get_version():
    from botaxon import __VERSION__
    return __VERSION__

BASEDIR_PATH = os.path.abspath(os.path.dirname(__file__))

setup(
    name="botaxon",
    version=get_version(),
    author="Geoffrey GUERET",
    author_email="geoffrey@gueret.tech",

    description="Taxonomic parser for (sub)species botanical names.",
    long_description=open(os.path.join(BASEDIR_PATH, "README.md"), "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ggueret/botaxon",
    license="MIT",

    packages=["botaxon"],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=["pytest==4.4.1", "pytest-cov==2.6.1"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
