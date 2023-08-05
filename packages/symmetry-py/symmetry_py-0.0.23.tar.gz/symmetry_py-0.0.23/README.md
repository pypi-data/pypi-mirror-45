# Symmetry Python

## Distribution and Publishing
1. Install twine if you haven't already done so: `pip install twine`.
2. Create a `~/.pypirc` file and add the following contents to it:
```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://upload.pypi.org/legacy/
username: dpinzaru
password: <AccountPassword>

[pypitest]
repository: https://testpypi.python.org/pypi
username: YOUR_USERNAME_HERE
password: YOUR_PASSWORD_HERE
```
3. After pushing your code to the remote repository create a new distribution by running `python setup.py sdist`.
4. To plubish the new distribution run `twine upload dist/*`.


## Virtual Environment
It is necessary to create a Virtual Env within the context of this project so that the package requirements are not 
cluttered by the global environment. Execute the following steps to create a virtual env for this project:
1. In the project root run `python -m venv env`. You might have to run `python3 -m venv env`.
2. Point your IDE to use the newly created environment in `./env` folder.
3. To test that your virtual env is setup properly run `which python`, the path should point to `.../symmetry_py/env/bin/python`.


