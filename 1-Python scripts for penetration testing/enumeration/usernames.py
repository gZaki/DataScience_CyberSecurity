#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019, Gouasmia Zakaria
# All rights reserved.

import sys


def get_names(filename):
    items = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\r\n')
            if line[0] == '#': continue
            if line == '': continue
            items.append(line)

    return items


#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------
patterns = ['flast', 'firstl', 'first.last']

if len(sys.argv) not in [4, 5]:
    print('Usage: usernames.py firsts lasts pattern [domain]')
    print('Valid patterns include {0}'.format(', '.join(patterns)))
    sys.exit()

# Get our pattern and verify it.
p = sys.argv[3]
if p not in patterns:
    print('Pattern must be one of {0}'.format(', '.join(patterns)))
    sys.exit()

# Get the domain if it exists
d = None
if len(sys.argv) == 5:
    d = sys.argv[4]

# Get name lists
fnames = get_names(sys.argv[1])
lnames = get_names(sys.argv[2])


# Build usernames
usernames = []
if p == 'flast':
    for f in 'abcdefghijklmnopqrstuvwxyz':
        for l in lnames:
            usernames.append("{0}{1}".format(f, l))

if p == 'firstl':
    for f in fnames:
        for l in 'abcdefghijklmnopqrstuvwxyz':
            usernames.append("{0}{1}".format(f, l))

if p == 'first.last':
    for f in fnames:
        for l in lnames:
            usernames.append("{0}{1}".format(f, l))

# Add domain if provided.
if d is not None:
    for u in usernames:
        print("{0}@{1}".format(u, d))
else:
    for u in usernames:
        print(u)
