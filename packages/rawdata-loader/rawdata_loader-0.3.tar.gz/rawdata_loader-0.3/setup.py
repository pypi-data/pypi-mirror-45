import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rawdata_loader",
    version="0.3",
    author="Noam Nisenholz",
    author_email="noamholz@guardian-optech.com",
    description="Tools for Guardian raw data handling",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)