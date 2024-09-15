#!/bin/bash

TARGET_DIRS=("../users_service")
LIB_NAME="ft_i18n"
LIB_FILENAME="${LIB_NAME:?}-0.1-py3-none-any.whl"
LIB_OUTPUT_DIR="dist"
LIB_FILE_PATH="${LIB_OUTPUT_DIR}/${LIB_FILENAME}"

rm -rf build/ ${LIB_OUTPUT_DIR}/ *.egg-info

echo "Building the wheel for the library..."
python3 setup.py bdist_wheel

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "${TARGET_DIR}" ]; then
        LIBS_DIR="${TARGET_DIR}/libs"
        if [ ! -d "${LIBS_DIR}" ]; then
            echo "Creating directory ${LIBS_DIR}..."
            mkdir -p "${LIBS_DIR}"
        fi
        echo "Removing old ${LIB_NAME} wheel file in ${LIBS_DIR}..."
        rm -rf "${LIBS_DIR:?}/${LIB_FILENAME}"
        echo "Copying ${LIB_NAME} wheel file to ${LIBS_DIR}..."
        cp "${LIB_FILE_PATH}" "${LIBS_DIR}"
    else
        echo "Error: Target directory ${TARGET_DIR} does not exist."
        exit 1
    fi
done

rm -rf build/ ${LIB_OUTPUT_DIR}/ *.egg-info


echo "Deployment of ${LIB_NAME} completed successfully."
