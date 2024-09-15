#!/bin/bash

TARGET_DIRS=("../users_service")
LIB_NAME="ft_i18n"
LIB_FILENAME="${LIB_NAME:?}-0.1-py3-none-any.whl"
LIB_FILE_PATH="dist/${LIB_FILENAME}"

rm -rf build/ dist/ *.egg-info

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "${TARGET_DIR}" ]; then
        echo "Removing old ${LIB_NAME} wheel file in ${TARGET_DIR}..."
        rm -rf "${TARGET_DIR:?}/libs/${LIB_FILENAME}"
    else
        echo "Error: Target directory ${TARGET_DIR} does not exist."
        exit 1
    fi
done

echo "Removal of ${LIB_NAME} completed successfully."
