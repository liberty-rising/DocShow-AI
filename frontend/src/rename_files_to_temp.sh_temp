#!/bin/bash

rename_file_temp() {
    for f in "$1"/*; do
        if [ -d "$f" ]; then
            # If it's a directory, recurse into it
            rename_file_temp "$f"
        elif [ -f "$f" ]; then
            # If it's a file, rename it
            local new_name="${f}_temp"
            mv "$f" "$new_name"
        fi
    done
}

# Start the renaming process from the current directory
rename_file_temp "."
