# simon-game

Python package for playing the game [Simon](https://en.wikipedia.org/wiki/Simon_(game))

## Table of Contents
1. [Motivation](#motivation)
2. [Installation](#installation)
3. [File Structure](#file-structure)
4. [Licensing, Authors, and Acknowledgements](#licensing)


## Motivation

## Installation

- Create a python3 virtual environment

    `python3 -m venv ./venv`

- Start virtual environment

    `source venv/bin/activate`

- Stop virtual environment

    `deactivate`

- Install project dependencies 

    > (virtual env must be started to install dependencies)
     
    `pip install -r requirements.txt`

## Create python package

```
python setup.py sdist

pip install twine

# commands to upload to the pypi test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ simon_game


# command to upload to the pypi repository
twine upload dist/*
pip install simon_game


```