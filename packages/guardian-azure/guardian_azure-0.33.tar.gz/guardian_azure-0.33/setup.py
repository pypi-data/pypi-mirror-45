import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guardian_azure",
    version="0.33",
    author="Noam Nisenholz",
    author_email="noamholz@guardian-optech.com",
    description="Azure Blob Storage interface for Guardian scripts",
    url="",
    packages=setuptools.find_packages(include=["guardian_azure.py"]),
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)