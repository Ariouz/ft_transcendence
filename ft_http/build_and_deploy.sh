#!/bin/bash

TARGET_DIRS=("../api_gateway" "../users_service")
LIB_NAME="ft_http"

echo "Building the wheel for the library..."
python setup.py bdist_wheel

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "${TARGET_DIR}" ]; then
        echo "Copying ft_http directory to ${TARGET_DIR}..."
        cp -r ../${LIB_NAME} ${TARGET_DIR}
    else
        echo "Error: Target directory ${TARGET_DIR} does not exist."
        exit 1
    fi
done

echo "Deployment of  completed successfully."
