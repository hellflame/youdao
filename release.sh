#!/bin/bash

python2 setup.py sdist bdist_egg bdist_wheel

python3 setup.py bdist_egg bdist_wheel
