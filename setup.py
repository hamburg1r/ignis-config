from setuptools import setup, find_packages

setup(
    name="ignis-desktop",
    version="0.1.0",
    package_dir={"": "desktop"},
    packages=find_packages(where="desktop"),
)