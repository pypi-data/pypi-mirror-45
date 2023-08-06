# rawdata-handler
Tools for handling Guardian's raw data

## Setting up the environment

### Python installations
Create conda env:
```
conda create -n mc_v2 python=3.6
```
Install python packages:
```
conda install pandas=0.22.0 numpy=1.15.4 matplotlib=2.1.2 scikit-learn=0.19.1
conda install -c conda-forge azure-storage-blob
pip install xgboost==0.82 rawdata_handler
```

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



