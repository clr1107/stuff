#!/bin/bash
# Usage: preproc.sh

m4 -P --define=m4__PYTHON3_PATH="$(which python3)" notesc.py.m4 > notesc.py
