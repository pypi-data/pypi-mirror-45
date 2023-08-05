import setuptools
from pathlib import Path

setuptools.setup(
    name="xoop",
    version="1.0.1",
    long_description=Path("README.md").read_text(),
    # long_description=""
    packages=setuptools.find_packages(exclude=[".vscode"])
)

