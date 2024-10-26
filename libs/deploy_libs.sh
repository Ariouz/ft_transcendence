#!/bin/bash

FILE_LIB_FT_I18N_NAME="ft_i18n-0.1-py3-none-any.whl"
FILE_LIB_FT_REQUESTS_NAME="ft_requests-0.1-py3-none-any.whl"

FILE_LIB_FT_I18N="./libs/built_wheels/ft_i18n-0.1-py3-none-any.whl"
FILE_LIB_FT_REQUESTS="./libs/built_wheels/ft_requests-0.1-py3-none-any.whl"

DEST_LIB_FT_I18N=("users_service" "pong_service")
DEST_LIB_FT_REQUESTS=("api_gateway" "users_service" "websocket_server" "libs/ft_i18n" "pong_service")

echo "Starting deployment process for library wheels."

copy_file() {
    local file=$1
    shift
    local destinations=("$@")
        
    for dest in "${destinations[@]}"; do
        final_dest_dir="${dest}/libs/"
        
        if [ ! -d "$final_dest_dir" ]; then
            echo "Directory $final_dest_dir does not exist. Creating the directory..."
            mkdir -p "$final_dest_dir"
        fi
        
        echo "Copying $file to $final_dest_dir..."
        cp "$file" "$final_dest_dir"
    done
    
    echo "Completed deployment for $file."
}

echo
echo "Deploying ${FILE_LIB_FT_I18N}..."
copy_file "$FILE_LIB_FT_I18N" "${DEST_LIB_FT_I18N[@]}"

echo
echo "Deploying ${FILE_LIB_FT_REQUESTS}..."
copy_file "$FILE_LIB_FT_REQUESTS" "${DEST_LIB_FT_REQUESTS[@]}"

echo
echo "Deployment of ${FILE_LIB_FT_I18N_NAME} and ${FILE_LIB_FT_REQUESTS_NAME} completed successfully."
