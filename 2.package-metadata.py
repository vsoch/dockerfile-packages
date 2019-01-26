#!/usr/bin/env python

from time import sleep
import requests
import pickle
import json
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

# If we've already started (or are updating)
if os.path.exists('pypi-metadata.pkl'):
    metadata = pickle.load(open('pypi-metadata.pkl', 'rb'))

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

pickle.dump(metadata, open('pypi-metadata.pkl', 'wb'))

################################################################################
# Apt Packages
################################################################################

from containertree.utils import run_command
# Not required = here is how I got the platform names
# Apt is not included!
# platforms = requests.get("https://libraries.io/api/platforms?api_key=%s" % token).json()

# for platform in platforms:
#    print(platform['name'])
# Go
# NPM
# Packagist
# Maven
# Pypi
# Rubygems
# NuGet
# Bower
# Wordpress
# CocoaPods
# CPAN
# Clojars
# Cargo
# CRAN
# Hackage
# Meteor
# Atom
# Hex
# Puppet
# PlatformIO
# Pub
# Homebrew
# Emacs
# SwiftPM
# Carthage
# Julia
# Sublime
# Dub
# Elm
# Racket
# Haxelib
# Nimble
# Alcatraz
# PureScript
# Inqlude

# Instead, let's use a docker container to install a package and get
# dependencies after. Kill subprocess if takes longer than 1 minute

import multiprocessing

apt = pickle.load(open('apt-tree.pkl', 'rb'))

def worker(package, return_dict):
    from containertree.utils import run_command
    command = ["docker", "run", "-it", "vanessa/ubuntu-dependencies:16.04", package]
    result = run_command(command)
    return_dict[package] = result['message']

aptmeta = dict()
#aptmeta = pickle.load(open('apt-metadata.pkl', 'rb'))
packages = apt.root.children.copy()
for i in range(377, int(len(packages) / 5)):

    # Grab 5 children to process
    children = []
    for c in range(5):
        package = packages.pop(0).label

        # Skip over those we've already done
        if package in aptmeta:
            continue

        print('Parsing %s, %s of %s' %(package, i, len(apt.root.children)))
        children.append(package)

    if len(children) == 0:
        continue

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    jobs = []
    for procnum in range(len(children)):
        p = multiprocessing.Process(target=worker, name="docker", args=(children[procnum], return_dict,))
        jobs.append(p)
        p.start()

    for proc in jobs:
        # Timeout of one minute
        proc.join(60)

        # If it's still going, kill it
        if proc.is_alive():
            print('%s terminated, skipping' % proc)
            proc.terminate()
            proc.join()

    for package, result in return_dict.items():
        dependencies = json.loads(result)
        print(dependencies)
        aptmeta[package] = dependencies

    pickle.dump(aptmeta, open('apt-metadata.pkl', 'wb'))

with open('apt-metadata.json', 'w') as filey:
    filey.writelines(json.dumps(aptmeta, indent=4))
