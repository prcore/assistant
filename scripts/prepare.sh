#!/bin/bash

mkdir -p ./data/log
mkdir -p ./data/docs
mkdir -p ./data/langchain
cp -r ./examples ./data
cp ./examples/example.env ./.env
nano ./.env
