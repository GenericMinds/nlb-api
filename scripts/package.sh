#!/bin/bash

while getopts t: flag
do
    case "${flag}" in
        t) SAM_TEMPLATE=${OPTARG};;
    esac
done


# This script is used for local development
sam build --template "${SAM_TEMPLATE}" --use-container

# Review through all compiled functions and remove layers.shared prefix for layer support
find '.aws-sam/build' -type f -name "*.py" -print0 | xargs -0 sed -i'' -e 's/functions.kits.//g'