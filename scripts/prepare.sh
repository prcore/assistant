#!/bin/bash

current_dir=${PWD##*/}
current_dir=${current_dir:-/}
if [ "$current_dir" != "scripts" ]; then
    echo "You are not in the scripts directory, exiting..."
    exit 1
fi

cd ..
mkdir -p ./data/log
mkdir -p ./data/docs
mkdir -p ./data/langchain
cp -r ./examples ./data
cp ./examples/example.env ./.env
nano ./.env
