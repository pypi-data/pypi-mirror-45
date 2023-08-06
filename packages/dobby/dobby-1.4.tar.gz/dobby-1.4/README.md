# Dobby
A tiny lambda handler generalizing framework for Python 

## Workflow

### Requirements
The `requirements.txt` states the required dependencies for the project.  
To install the requirements (preferably in the [active virtual environment](https://docs.python-guide.org/dev/virtualenvs/)) run `pip install -r requirements.txt`  

### Installation
Run `pip install dobby` to install the package for usage.

### Scripts
The workflow scripts for the project are provided using [`pyinvoke`](http://www.pyinvoke.org/).  

| Command | Purpose |  
| --- | --- |
| `invoke --list` | Shows the list of available commands |  
| `invoke test` | Runs all the tests for the package |  
| `invoke clean-cache` | Removes all the `__pycache__/` and `.pytest_cache/` files |  

## Publish package 
To publish a new version of the package use [`this tutorial`](https://packaging.python.org/tutorials/packaging-projects/).  

