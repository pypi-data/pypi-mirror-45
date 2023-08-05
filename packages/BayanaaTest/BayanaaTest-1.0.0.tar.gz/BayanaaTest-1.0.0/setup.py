import setuptools
from pathlib import Path

setuptools.setup(
    name = "BayanaaTest",
    version= "1.0.0",
    packages = setuptools.find_packages(exclude = [".vscode"])
)