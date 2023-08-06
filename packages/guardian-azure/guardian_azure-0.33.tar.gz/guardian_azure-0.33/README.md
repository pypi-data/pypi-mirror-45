# guardian_azure
Azure Blob Storage interface for Guardian scripts

## Setting up the environment

conda install -c conda-forge azure-storage-blob


## Instructions for exporting a new version to PyPI
Find further important info at:  
https://packaging.python.org/tutorials/packaging-projects/  
https://python-packaging.readthedocs.io/en/latest/minimal.html  

update packaging & uploading tools
```
pip install --user --upgrade setuptools wheel
python -m pip install --user --upgrade twine
```

After creating the appropriate files structure for the package, perform:
```
python setup.py sdist
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

Finally, enter the required PyPI credentials (currently using "guardian-optech" account)



