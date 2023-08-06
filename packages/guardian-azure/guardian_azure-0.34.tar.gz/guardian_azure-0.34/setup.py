import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guardian_azure",
    version="0.34",
    author="Noam Nisenholz",
    author_email="noamholz@guardian-optech.com",
    description="Azure Blob Storage interface for Guardian scripts",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)