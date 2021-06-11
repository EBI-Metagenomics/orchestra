# Orchestra

## Developing

### Requirements

- Python >=3.8
- Docker and Docker Compose (optional)

### Create a python virtual env

Using venv

```bash
python -m venv venv     # create python environment
source ./venv/bin/activate    # activate python enviroment
```

Using conda

```bash
conda create -n orchestra python=3.8    # create python environment
conda activate orchestra    # activate python enviroment
```

### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Install dependencies

```bash
python3 scripts/setup_env.py
```

### Install Pre commit hooks

This installs hooks for running python's black formatter and flake8 lint

```bash
pre-commit install
```

Now, refer to the `README` of the specific project you want to work on.
