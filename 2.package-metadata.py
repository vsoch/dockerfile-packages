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
# dependencies after

aptmeta = dict()
for p in range(0, len(apt.root.children)):
    node = apt.root.children[p]
    package = node.label

    # Skip over those we've already done
    if package in aptmeta:
        continue

    print('Parsing %s, %s of %s' %(package, p, len(apt.root.children)))
    command = ["docker", "run", "-it", "vanessa/apt-package-dependencies", package]
    result = run_command(command)
    lines = result['message'].split('\r\n')

    dependencies = dict()

    # First line is the package name
    current = ""
    for l in range(1, len(lines)):
        line = lines[l]
        if not line:
            continue
        if "Depends" in line:
            current = "Depends"
            line = line.replace('Depends:', '').split()
        elif "Suggests" in line:
            current = "Suggests"
            line = line.replace('Suggests:', '').split()
        elif "Replaces" in line:
            current = "Replaces"
            line = line.replace('Replaces:', '').split()
        else:
            line = line.strip()
        if current not in dependencies:
            dependencies[current] = []
        if isinstance(line, list):
            line = line[0]
        # Clean up
        line = line.strip('|').strip('&')
        dependencies[current].append(line)

    aptmeta[package] = dependencies
    print(dependencies)
