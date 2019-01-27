#!/bin/bash

# Read in arguments
OUTPUT="${1}"
URI="${2}"
CACHE_DIR="${3}"

container-diff analyze "${URI}" --type=pip --type=apt --type=history --json --quiet --cache-dir "${CACHE_DIR}" --no-cache --verbosity=panic --output "${OUTPUT}"

# container-diff analyze docker://alerta/alerta-web  --type=pip --type=apt --type=history --json --quiet --cache-dir /scratch/users/vsochat/.singularity/docker --verbosity=panic --output /scratch/users/vsochat/WORK/dockerfiles/container-diff/alerta-alerta-web.json
