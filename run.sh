#!/bin/bash

set -e # exit if a command fails

# Prepare dictionariess
if [ ! -d "data" ]; then
  mkdir data
fi

if [ ! -d "dictionaries" ]; then
  mkdir dictionaries
fi

python3 main.py