#!/usr/bin/python

import json

repo_file = '/etc/yum.repos.d/redhat.repo'
test_dict = dict()
lines = open(repo_file, 'r').read().split('\n')
current_repo = None

for line in lines:
  if line.strip() != '':
    if line.startswith('#'):
      pass
    elif line.startswith('['):
      current_repo = line.replace('[','')
      current_repo = current_repo.replace(']','')
      test_dict[current_repo] = dict()
    else:
      k, v = line.split("=")
      test_dict[current_repo][k.strip()] = v.strip()