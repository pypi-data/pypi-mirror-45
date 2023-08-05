import setuptools
from pathlib import Path

setuptools.setup(
  name = "martinmymath",
  versio = "1.0.0",
  long_description=Path("readme.md").read_text(),
  package = setuptools.find_packages(exclude=[".vscode"])

)