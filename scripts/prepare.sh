#!/bin/bash

current_dir=${PWD##*/}
current_dir=${current_dir:-/}
if [ "$current_dir" != "scripts" ]; then
    echo "You are not in the scripts directory, exiting..."
    exit 1
fi

bash mkdir.sh
cd ..
nano ./.env
nano ./data/intro.txt
nano ./data/magic.txt
nano ./data/prompt.txt
nano ./data/sidebar.txt
