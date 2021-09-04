#!/bin/bash

# This script is used for local development
sam build --template template.yaml --use-container

# Review through all compiled functions and remove layers.shared prefix for layer support
find '.aws-sam/build' -type f -name "*.py" -print0 | xargs -0 sed -i'' -e 's/functions.kits.//g'

sam deploy --guided