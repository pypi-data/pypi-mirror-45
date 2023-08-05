import os
from setuptools import setup


def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="simon_game",
    version="0.0.2",
    description="command line simon game",
    license='MIT',
    author="Darryl Balderas",
    author_email="drrylbalderas@gmail.com",
    url="https://github.com/darrylbalderas/simon-game",
    packages=['simon_game'],
    entry_points={
        'console_scripts': [
            'simon_game=simon_game:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ]
)