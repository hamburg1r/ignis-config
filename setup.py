from setuptools import setup, find_packages

setup(
    name="ignis-desktop",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        'desktop': [
            'style.scss',
            'scss/general.scss',
            'scss/osd.scss',
            'scss/search.scss'
        ],
    },
    include_package_data=True,
)