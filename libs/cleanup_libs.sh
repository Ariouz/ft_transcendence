#!/bin/bash

FILE_LIB_FT_I18N="ft_i18n-0.1-py3-none-any.whl"
FILE_LIB_FT_REQUESTS="ft_requests-0.1-py3-none-any.whl"

DEST_LIB_FT_I18N=("users_service" "pong_service")
DEST_LIB_FT_REQUESTS=("users_service" "websocket_server" "libs/ft_i18n" "pong_service")

echo "Starting cleanup process for libraries."

remove_file() {
    local file=$1
    shift
    local destinations=("$@")
        
    for dest in "${destinations[@]}"; do
        final_dest="${dest}/libs/${file}"
        if [ -f "$final_dest" ]; then
            echo "Removing $final_dest..."
            rm "$final_dest"
        else
            echo "File $final_dest does not exist. Skipping..."
        fi
    done
    
    echo "Completed removal attempts for $file."
}

echo
echo "Removing ${FILE_LIB_FT_I18N} from destinations..."
remove_file "$FILE_LIB_FT_I18N" "${DEST_LIB_FT_I18N[@]}"

echo
echo "Removing ${FILE_LIB_FT_REQUESTS} from destinations..."
remove_file "$FILE_LIB_FT_REQUESTS" "${DEST_LIB_FT_REQUESTS[@]}"

echo
echo "Cleanup of ${FILE_LIB_FT_I18N} and ${FILE_LIB_FT_REQUESTS} completed successfully."
