#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a package name to install."
fi

PACKAGE="${1}"

# Install the package
{
apt-get update && apt-get install -y ${PACKAGE}
} > /dev/null 2>&1

python /apt-cache.py ${PACKAGE}
