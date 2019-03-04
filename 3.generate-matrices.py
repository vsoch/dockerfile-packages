#!/usr/bin/env python

import pickle
import os
from glob import glob

# module load python/3.6.1
# ml py-ipython/6.1.0_py36

# First, let's read in both years data and get a set of unique container uris

containers_2019 = pickle.load(open('dockerfiles-01-13-2019.pkl','rb'))
containers_2017 = pickle.load(open('dockerfiles-02-16-2017.pkl','rb'))

print(len(containers_2017))
print(len(containers_2019))

# 129463
# 423541

containers = set()

if os.path.exists('dockerfiles-2017+2019.pkl'):
    containers = pickle.load(open('dockerfiles-2017+2019.pkl', 'rb'))

else:
    for container in containers_2017 + containers_2019:
        containers.add(container)

    pickle.dump(containers, open('dockerfiles-2017+2019.pkl','wb'))

print(len(containers))
# 505234

################################################################################
# Pip Trees!
################################################################################

# For each, build an apt and pip tree
from containertree import ContainerPipTree

pip = ContainerPipTree()

# Parse output files from container-diff
diffs = glob('container-diff/*.json')
pickle.dump(diffs, open('diffs.pkl','wb'))

# len(diffs)
#  187449

seen = set()
for diff in diffs:
    tag = os.path.basename(diff).replace('-','/', 1).replace('.json','')
    if tag in seen:
        continue
    seen.add(tag)
    try:
        pip.update(diff, tag=tag)
    except TypeError:
        pass
    except: #JSONDecodeError:
        pass

# Next add scraped containers from 2017-2019
count = 0
for container in containers:

    if container in pip.root.tags:
        continue

    if count % 1000 == 0:
        pickle.dump(pip, open('pip-tree-x.pkl', 'wb'))
        pickle.dump(seen, open('seen-containers.pkl', 'wb'))

    if container in seen:
        continue

    print('Adding %s' % container)
    try:
        pip.update(container, tag=container)
    except TypeError:
        pass

    seen.add(container)
    count +=1

pickle.dump(pip, open('pip-tree-x.pkl', 'wb'))
pickle.dump(seen, open('seen-containers.pkl', 'wb'))

################################################################################
# Apt Trees!
# We don't have metadata for apt so its not the analysis focus
################################################################################

from containertree import ContainerAptTree

apt = ContainerAptTree()

seen = []
for diff in diffs:
    tag = os.path.basename(diff).replace('-','/', 1).replace('.json','')
    if tag in seen:
        continue
    seen.append(tag)
    try:
        apt.update(diff, tag=tag)
    except TypeError:
        pass
    except: #JSONDecodeError:
        pass

# len(pip.root.tags)
# 56525
# len(pip.root.children) -> 6387

# We would need to extract these packages... takes too long on local machine.
# Next add scraped containers from 2017-2019
count = 1000
for container in containers:

    if container in pip.root.tags:
        continue

    if count % 1000 == 0:
        pickle.dump(pip, open('pip-tree.pkl', 'wb'))

    if container in seen:
        continue

    print('Adding %s' % container)
    try:
        pip.update(container, tag=container)
    except TypeError:
        pass

    seen.add(container)
    count +=1

pickle.dump(pip, open('pip-tree.pkl', 'wb'))
pickle.dump(seen, open('seen-containers.pkl', 'wb'))







# Stopped at count 53854
# container
# 'booyaabes/kali-linux-full'
# see seen.pkl to pick up, we are good to start with a set of this size:
# len(seen) -> 19,501
# len(apt.root.tags) -> 6025
# len(pip.root.tags) -> 3685

# Generate matrices for both
pip_vectors = pip.export_vectors()
# pip_vectors.shape
# (3685, 1917)
pip_vectors = pip_vectors.fillna(0)
pip_vectors.to_csv('pip-vectors.csv')
pip_vectors.to_pickle('pip-vectors.pkl')

# vectors.shape (69380, 7046)
vectors.to_csv('pip-vectors-3-3-2019.csv')
vectors.to_pickle('pip-vectors-3-3-2019.pkl')
vectors = vectors.fillna(0)
vectors.to_sparse()

apt_vectors = apt.export_vectors()
# apt_vectors.shape
# (6025, 17194)
apt_vectors = apt_vectors.fillna(0)
apt_vectors.to_csv('apt-vectors.csv')
apt_vectors.to_pickle('apt-vectors.pkl')

################################################################################
# Apt Trees!
################################################################################

# For each, build an apt and pip tree
from containertree import ContainerAptTree

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

pickle.dump(apt, open('apt-tree.pkl', 'wb'))
pickle.dump(pip, open('pip-tree.pkl', 'wb'))
pickle.dump(seen, open('seen-containers.pkl', 'wb'))

# Stopped at count 53854
# container
# 'booyaabes/kali-linux-full'
# see seen.pkl to pick up, we are good to start with a set of this size:
# len(seen) -> 19,501
# len(apt.root.tags) -> 6025
# len(pip.root.tags) -> 3685

# Generate matrices for both
pip_vectors = pip.export_vectors()
# pip_vectors.shape
# (3685, 1917)
pip_vectors = pip_vectors.fillna(0)
pip_vectors.to_csv('pip-vectors.csv')
pip_vectors.to_pickle('pip-vectors.pkl')

apt_vectors = apt.export_vectors()
# apt_vectors.shape
# (6025, 17194)
apt_vectors = apt_vectors.fillna(0)
apt_vectors.to_csv('apt-vectors.csv')
apt_vectors.to_pickle('apt-vectors.pkl')
