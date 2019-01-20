#!/usr/bin/env python

from time import sleep
import requests
import pickle
import os
import sys

################################################################################
# Pip Packages
################################################################################

pip = pickle.load(open('pip-tree.pkl', 'rb'))

# Ensure we have environment variable exported for libraries.io
# Note that rate limit is 60/min (one per second)
# see https://libraries.io/api
token = os.environ.get('LIBRARIESIO_TOKEN')
if token == None:
    print('Please export LIBRARIESIO_TOKEN from https://libraries.io/account')
    sys.exit(1)

# Load in package matrix for Pypi.
metadata = dict()

# Note - this had connection resets a few times
# For each package, get metadata
for p in range(0, len(pip.root.children)):
    node = pip.root.children[p]
    package = node.label

    # Skip over those we've already done
    if package in metadata:
        continue

    print('Parsing %s, %s of %s' %(package, p, len(pip.root.children)))
    response = requests.get('https://pypi.org/pypi/%s/json' % package)

    # Problem retrieving from pypi
    if response.status_code != 200:
        print("Problem getting %s from pypi." % package)
        continue

    metadata[package] = response.json()
 
    # Get dependencies via https://libraries.io/api
    url = "https://libraries.io/api/Pypi/%s/latest/dependencies?api_key=%s" %(package, token)
    response = requests.get(url)
    libio = response.json()
    libio['url'] = url
    metadata[package]['librariesio'] = libio
    sleep(1.1)


with open('pypi-metadata.json', 'w') as filey:
    filey.writelines(json.dumps(metadata, indent=4))

pickle.dump(metadata, open('pypi-metadata.json', 'wb'))

################################################################################
# Apt Packages
################################################################################

# Load in apt packages
apt = pickle.load(open('apt-tree.pkl', 'rb'))
