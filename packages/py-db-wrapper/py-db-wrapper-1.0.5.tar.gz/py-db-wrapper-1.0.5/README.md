# py-db-wrapper
Shallow wrapper for convenience tools for db management


## Developer notes

Package deployment etc

```sh
python setup.py test
```

```sh
python setup.py sdist bdist_egg
```
```sh
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```