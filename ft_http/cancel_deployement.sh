#!/bin/bash

TARGET_DIRS=("../api_gateway" "../users_service" "../websocket_server")
LIB_NAME="ft_http"
LIB_FILENAME="ft_http-0.1-py3-none-any.whl"
LIB_FILE_PATH="dist/${LIB_FILENAME}"

rm -rf "build"
rm -rf "dist"
rm -rf "${LIB_NAME:?}/ft_http.egg-info"
rm -rf "ft_http.egg-info"

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "${TARGET_DIR}" ]; then
        echo "Removing old ${LIB_NAME} wheel file in ${TARGET_DIR}..."
        rm -rf "${TARGET_DIR:?}/${LIB_FILENAME}"
    else
        echo "Error: Target directory ${TARGET_DIR} does not exist."
        exit 1
    fi
done

echo "Removal of ${LIB_NAME} completed successfully."
