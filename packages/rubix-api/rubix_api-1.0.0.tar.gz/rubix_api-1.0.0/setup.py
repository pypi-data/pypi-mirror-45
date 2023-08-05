import imp
import os
import pathlib
from setuptools import setup

# Kept manually in sync with rubix_api.__version__
version = imp.load_source('rubix_api.version', os.path.join('rubix_api', '__init__.py')).__version__

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="rubix_api",
    version=version,
    description="Indoor api to interact with Rubix",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rubix-labs/rubix-api",
    author="HasanJ",
    author_email="hasan_sg@hotmail.com",
    packages=["rubix_api"],
    include_package_data=True,
    install_requires=["requests"],
)