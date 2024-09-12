#!/bin/bash

TARGET_DIRS=("../api_gateway" "../users_service" "../websocket_server")
LIB_NAME="ft_requests"
LIB_FILENAME="${LIB_NAME:?}-0.1-py3-none-any.whl"
LIB_FILE_PATH="dist/${LIB_FILENAME}"

rm -rf "build"
rm -rf "dist"
rm -rf "${LIB_NAME:?}/${LIB_NAME:?}.egg-info"
rm -rf "${LIB_NAME:?}.egg-info"

echo "Building the wheel for the library..."
python3 setup.py bdist_wheel

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "${TARGET_DIR}" ]; then
        echo "Removing old ${LIB_NAME} wheel file in ${TARGET_DIR}..."
        rm -rf "${TARGET_DIR:?}/${LIB_FILENAME}"
        echo "Copying ${LIB_NAME} wheel file to ${TARGET_DIR}..."
        cp "${LIB_FILE_PATH}" "${TARGET_DIR}"
    else
        echo "Error: Target directory ${TARGET_DIR} does not exist."
        exit 1
    fi
done

echo "Deployment of ${LIB_NAME} completed successfully."
