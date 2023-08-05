from setuptools import setup, find_packages

long_desc = 'A Geometry Dash API Wrapper written in Python. Geometry Dash is a game created by RobTopGames. :)'

setup(
    name = 'gd.py',
    packages = ['gd', 'gd.utils'],
    version = '0.0.1.1',
    description = 'A Geometry Dash API wrapper for Python',
    long_description = long_desc,
    author = 'NeKitDSS',
    author_email = 'nekitguypro@gmail.com',
    url = 'https://github.com/NeKitDSS/gd.py',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
    ]
)
