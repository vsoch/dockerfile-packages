#!/usr/bin/env python

import pickle

# First, let's read in both years data and get a set of unique container uris

containers_2019 = pickle.load(open('dockerfiles-01-13-2019.pkl','rb'))
containers_2017 = pickle.load(open('dockerfiles-02-16-2017.pkl','rb'))

print(len(containers_2017))
print(len(containers_2019))

# 129463
# 423541

containers = set()

containers.index(container)
for container in containers_2017 + containers_2019:
    containers.add(container)

print(len(containers))

# 505234
pickle.dump(containers, open('dockerfiles-2017+2019.pkl','wb'))


################################################################################
# Trees!
################################################################################

# For each, build an apt and pip tree
from containertree import ContainerPipTree, ContainerAptTree

apt = ContainerAptTree()
pip = ContainerPipTree()
seen = set()

count = 1000
for container in containers:

    if container in apt.root.tags:
        continue

    if count % 1000 == 0:
        pickle.dump(apt, open('apt-tree.pkl', 'wb'))
        pickle.dump(pip, open('pip-tree.pkl', 'wb'))

    if container in seen:
        continue

    print('Adding %s' % container)
    try:
        apt.update(container, tag=container)
    except TypeError:
        pass
    try:
        pip.update(container, tag=container)
    except TypeError:
        pass

    seen.add(container)
    count +=1

#TODO: stopped here:
# 1. check on arxiv runs
# 2. when we are done parsing Github orgs from the api (for dockerfiles) run then through Git cloning
# 3. when container apt/pip trees done, export various datas and write up.
