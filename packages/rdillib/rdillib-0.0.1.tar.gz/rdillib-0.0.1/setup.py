import setuptools

# Read the long description:
with open("README.md", mode="r") as FILE_HANDLER:
    LONG_DESCRIPTION = FILE_HANDLER.read()

# Package version:
VERSION = "0.0.1"

setuptools.setup(
    name="rdillib",
    version=VERSION,
    author="area4 Team",
    author_email="me@rdil.rocks",
    description="Private utility",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://rdil.rocks",
    packages=setuptools.find_packages(),
    include_package_data=True
)
