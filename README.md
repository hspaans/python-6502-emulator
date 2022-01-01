# python-template

## Using devcontainer

Valid variant options are: lastest, 3, 3.9, 3.8, 3.7

```json
  "build": {
    "dockerfile": "Dockerfile",
    "args": {
      "VARIANT": "3",
      "INSTALL_NODE": "true",
      "NODE_VERSION": "lts/*"
    }
  },
```

## Linters

### Using Pylint

```json
  "settings": {
    "python.linting.banditEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.linting.pylintEnabled": true,
  }
```

### Using Bandit

```json
  "settings": {
    "python.linting.banditEnabled": true,
    "python.linting.flake8Enabled": false,
    "python.linting.pylintEnabled": false,
  }
```

```shell
$ bandit-config-generator -o .bandit.yml
[ INFO]: Successfully wrote profile: .bandit.yml
```

### Using Flake8

```json
  "settings": {
    "python.linting.banditEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
  }
```

`.flake8`

```toml
[flake8]
ignore =
    D203
    D400
    D401
    E501
exclude =
    .git,
    __pycache__,
    docs/source/conf.py,
    old,
    build,
    dist,
    .venv
max-complexity = 10
```

## Django

```shell
$ pip3 install --user django
$ django-admin startproject myproject .
...
```

[flake8-config]: https://flake8.pycqa.org/en/latest/user/configuration.html
[pylint-config]: https://pylint.pycqa.org/en/latest/user_guide/options.html
