#!/usr/bin/env python

import os
import sys
import json
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)


# Helper Functions

def run_command(command):
    '''run_command uses subprocess to send a command to the terminal.
       Parameters
       ==========
       command: the command to send, should be a list for subprocess
    '''
    try:
        output = Popen(command, stderr=STDOUT, stdout=PIPE)

    except FileNotFoundError:
        command.pop(0)
        output = Popen(command, stderr=STDOUT, stdout=PIPE)

    t = output.communicate()[0],output.returncode
    output = {'message':t[0],
              'return_code':t[1]}

    if isinstance(output['message'], bytes):
        output['message'] = output['message'].decode('utf-8')

    return output


def main():

    if len(sys.argv) == 1:
        print('Please provide a package name.')
        sys.exit(1)

    package = sys.argv[1]

    # Get the dependencies
    result = run_command(["apt-cache", "depends", package])
    lines = result['message'].split('\n')
    dependencies = dict()

    # First line is the package name
    current = ""
    for l in range(1, len(lines)):
        line = lines[l]
        if not line:
            continue

        # The first line has a pipe
        line = line.strip().strip('|').strip('&')

        if "Breaks" in line:
            current = "Breaks"
            line = line.replace('Breaks:', '').split()

        if "PreDepends" in line:
            current = "PreDepends"
            line = line.replace('PreDepends:', '').split()

        elif "Conflicts" in line:
            current = "Conflicts"
            line = line.replace('Conflicts:', '').split()

        elif "Depends" in line:
            current = "Depends"
            line = line.replace('Depends:', '').split()

        elif "Suggests" in line:
            current = "Suggests"
            line = line.replace('Suggests:', '').split()

        elif "Replaces" in line:
            current = "Replaces"
            line = line.replace('Replaces:', '').split()

        elif "Recommends" in line:
            current = "Recommends"
            line = line.replace('Recommends:', '').split()

        if current not in dependencies:
            dependencies[current] = []
        if isinstance(line, list):
            line = line[0]

        line = line.strip()

        if len(line) > 0:
            dependencies[current].append(line)

    print(json.dumps(dependencies))

if __name__ == '__main__':
    main()
