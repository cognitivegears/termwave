"""Setup script for termwave package."""

from setuptools import setup, find_packages

setup(
    name="termwave",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "termwave=src.main:main",
        ],
    },
)