import os
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
VERSION = "VERSION-NOT-FOUND"
for line in (HERE / "snails" / "__init__.py").read_text().split("\n"):
    if line.startswith("__version__"):
        VERSION = eval(line.split("=")[-1])
README = (HERE / "README.rst").read_text()
REQUIREMENTS = [
    "aiosmtpd"
]

if __name__ == "__main__":
    setup(
        name="snails",
        version=VERSION,
        description="minimal smtpd handler",
        long_description=README,
        long_description_content_type="text/x-rst",
        author="Joe Cross",
        author_email="joe.mcross@gmail.com",
        url="https://github.com/numberoverzero/snails",
        license="MIT",
        platforms="any",
        include_package_data=True,
        packages=find_packages(exclude=("docs", "examples", "scripts", "tests")),
        install_requires=REQUIREMENTS,
    )
