#!/bin/bash

LIB_NAME="ft_i18n"
LIB_FILENAME="${LIB_NAME:?}-0.1-py3-none-any.whl"
LIB_OUTPUT_DIR="dist"

rm -rf build/ ${LIB_OUTPUT_DIR}/ *.egg-info

echo "Building the wheel for ${LIB_NAME}..."

python3 setup.py bdist_wheel

rm -rf build/ *.egg-info

echo
echo "Build of ${LIB_NAME} completed successfully."
