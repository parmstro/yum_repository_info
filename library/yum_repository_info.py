#!/usr/bin/python
# Copyright: (c) 2022, Paul Armstrong <parmstro@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from importlib.resources import path
from typing import ValuesView
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yum_repository_info

short_description: This module accepts a filespec for a yum repo file and returns a dictionary with the configuration

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: A repo file can contain meta data on multiple repos from a variety of sources. This information constitutes one of the views on the content available for the host that we are examining. This module reads the information from a provided repo file defined by path and returns a dictionary called content_view. This maps to familiar terminology from foreman.

options:
    path:
        description: The path to the yum repo file to gather the metadata from
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - parmstro.utilities.yum_repository_info

author:
    - Paul Armstrong (@parmstro)
'''

EXAMPLES = r'''
# Read a repo file
- name: Get the Red Hat repo view
  parmstro.utilities.yum_repository_info:
    name: "/etc/yum.repos.d/redhat.repo"

'''

RETURN = r'''
# The repo file contents rendered as a dictionary
content_view:
    description: The dictionary containing the repo configuration
    type: dict
    returned: always
    sample: |
      view:
        rhel-8-for-x86_64-baseos-rpms: 
          name: "Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)"
          baseurl: "https://sat6.parmstrong.ca/pulp/repos/Default_Organization/Library/content/dist/rhel8/$releasever/x86_64/baseos/os"
          enabled: "1"
          gpgcheck: "1"
          gpgkey: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release"
          sslverify: "1"
          sslcacert: "/etc/rhsm/ca/katello-server-ca.pem"
          sslclientkey: "/etc/pki/entitlement/7761031002674669954-key.pem"
          sslclientcert: "/etc/pki/entitlement/7761031002674669954.pem"
          metadata_expire: "1"
          enabled_metadata: "1"
        rhel-8-for-x86_64-appstream-rpms:
          name: "Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)"
          baseurl: "https://sat6.parmstrong.ca/pulp/repos/Default_Organization/Library/content/dist/rhel8/$releasever/x86_64/appstream/os"
          enabled: "1"
          gpgcheck: "1"
          gpgkey: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release"
          sslverify: "1"
          sslcacert: "/etc/rhsm/ca/katello-server-ca.pem"
          sslclientkey: "/etc/pki/entitlement/7761031002674669954-key.pem"
          sslclientcert: "/etc/pki/entitlement/7761031002674669954.pem"
          metadata_expire: "1"
          enabled_metadata: "1"
        satellite-tools-6.10-for-rhel-8-x86_64-rpms: 
          name: "Red Hat Satellite Tools 6.10 for RHEL 8 x86_64 (RPMs)"
          baseurl: "https://sat6.parmstrong.ca/pulp/repos/Default_Organization/Library/content/dist/layered/rhel8/x86_64/sat-tools/6.10/os"
          enabled: "1"
          gpgcheck: "1"
          gpgkey: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release"
          sslverify: "1"
          sslcacert: "/etc/rhsm/ca/katello-server-ca.pem"
          sslclientkey: "/etc/pki/entitlement/7761031002674669954-key.pem"
          sslclientcert: "/etc/pki/entitlement/7761031002674669954.pem"
          metadata_expire: "1"
          enabled_metadata: "1"
'''

from ansible.module_utils.basic import AnsibleModule
from os.path import exists

def validate_path(path_spec):
  # make sure that a valid path has been provide
  repo_file_exists = exists(path_spec)
  return repo_file_exists


def run_module():
    # available arguments/parameters that can be passed to the module
    module_args = dict(
        path=dict(type='str', required=True),
    )

    # this is an *_info module, we need to return a results dictionary
    # initialize result
    result = dict(
        changed=False,
        failed=False,
        repo_view='[]'
    )

    # the module modifies nothing
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # return the current
    if module.check_mode:
        module.exit_json(**result)

    # 
    import json
    
    # validate repo file exists
    if validate_path(module.params["path"]) == False:
      module.fail_json(msg='The path does not exist', **result)

    test_dict = dict()
    lines = open(module.params["path"], 'r').read().split('\n')
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

    result['changed'] = True
    result['failed'] = False
    result['repo_view'] = test_dict

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()


