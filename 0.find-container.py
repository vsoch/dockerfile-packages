#!/usr/bin/env python

from sregistry.utils import run_command
import json
import pickle

# Read in list of prefixes

words = json.load(open('search-terms.json','r'))

containers = {}
count = 0
start = 0
for w in range(start, len(words)):
    word = words[w]
    res = run_command(['docker', 'search', '--limit', '100', word])

    if res['return_code'] == 0:
        res = res['message']
        lines = res.split('\n')[1:-1]
        for line in lines:
            container = line.split(' ')[0].strip()
            description = ' '.join([x for x in line.split(' ')[1:] if x]).strip('0')
            if container not in containers and len(description) > 0:
                num = len(containers) + 1
                print("Adding %sth container, %s" %(num, container))
                containers[container] = description
    count+=1

# One final save!
pickle.dump(containers, open('dockerfiles-01-13-2019.pkl' %save_index, 'wb'))
