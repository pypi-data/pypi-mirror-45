
from setuptools import setup, find_packages

setup(
    name = "ocspy",
    version = "0.0.4",
    keywords = ("pip", "optical communication","coherent optical", "ocspy", "ocspy"),
    description = "simulate optical communication",
    long_description = "simulate optical communication",
    license = "MIT Licence",
    package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.mat'],

        },

    url = "",
    author = "nigulasikaochuan",
    author_email = "nigulasikaochuan@sjtu.edu.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
