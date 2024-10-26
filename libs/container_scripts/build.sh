#!/bin/bash

LIB_NAMES=("ft_requests" "ft_i18n")
WHEEL_OUTPUT_DIR="built_wheels"

mkdir -p "${WHEEL_OUTPUT_DIR}"

build_libs() {
    local libs=("$@")
    for lib_dir in "${libs[@]}"; do
        local lib_filename="${lib_dir}-0.1-py3-none-any.whl"
        local lib_output_dir="${lib_dir}/dist"
        local lib_file_path="${lib_output_dir}/${lib_filename}"
        local lib_build_script="build.sh"

        cd "${lib_dir}" || { echo "Error: Failed to enter directory ${lib_dir}"; exit 1; }
        
        sh "./${lib_build_script}"
        if [[ $? -ne 0 ]]; then
            echo "Error: ${lib_build_script} failed for ${lib_dir}"
            exit 1
        fi

        cd ".." || { echo "Error: Failed to return to the parent directory"; exit 1; }
        
        mv "${lib_file_path}" "${WHEEL_OUTPUT_DIR}" || { echo "Error: Failed to move ${lib_file_path} to ${WHEEL_OUTPUT_DIR}"; exit 1; }
        rmdir "${lib_output_dir}"
        
        echo
        echo "Wheel of ${lib_dir} stored in ${WHEEL_OUTPUT_DIR}."
    done
    return 0
}

build_libs "${LIB_NAMES[@]}"

echo
echo "All libraries built and stored successfully in ${WHEEL_OUTPUT_DIR}."
echo "Note: The container will now stop as expected after building the libraries."
echo

exit 0

