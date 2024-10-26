#!/bin/bash

LIB_NAMES=("ft_requests" "ft_i18n")
WHEEL_OUTPUT_DIR="built_wheels"

echo "Starting cleanup process for libraries in ${WHEEL_OUTPUT_DIR}."

if [ ! -d "${WHEEL_OUTPUT_DIR}" ]; then
    echo "Directory ${WHEEL_OUTPUT_DIR} does not exist. No cleanup necessary."
    exit 0
fi

echo "Removing all files in the directory: ${WHEEL_OUTPUT_DIR}"
rm -f "${WHEEL_OUTPUT_DIR}"/*

echo "Attempting to remove the directory: ${WHEEL_OUTPUT_DIR}"
rmdir "${WHEEL_OUTPUT_DIR}" 2>/dev/null || { 
    echo "${WHEEL_OUTPUT_DIR} is not empty. Forcefully removing the directory and its contents."
    rm -rf "${WHEEL_OUTPUT_DIR}"
}

echo "Cleanup process completed successfully."

exit 0
