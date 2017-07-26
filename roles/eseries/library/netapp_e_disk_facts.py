#!/usr/bin/python

# (c) 2016, NetApp, Inc
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: netapp_e_facts
version_added: '2.3'
short_description: Get facts about NetApp E-Series arrays
extends_documentation_fragment:
    - netapp.eseries

description:
    - Return various information about NetApp E-Series storage arrays (eg, configuration, disks)

author: Kevin Hulquest (@hulquest)
'''

EXAMPLES = """
---
    - name: Get array facts
      netapp_e_disk_facts:
        array_id: "{{ netapp_array_id }}"
        api_url: "{{ netapp_api_url }}"
        api_username: "{{ netapp_api_username }}"
        api_password: "{{ netapp_api_password }}"
        validate_certs: "{{ netapp_api_validate_certs }}"
"""

RETURN = """
msg:
    description: Gathered facts for <StorageArrayId>.
    returned: always
    type: string
"""

from ansible.module_utils.api import basic_auth_argument_spec
from ansible.module_utils.basic import AnsibleModule, get_exception
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.urls import open_url

import collections
import json


def main():
    argument_spec = basic_auth_argument_spec()
    argument_spec.update(
        api_username=dict(type='str', required=True),
        api_password=dict(type='str', required=True, no_log=True),
        api_url=dict(type='str', required=True),
        ssid=dict(required=True)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    p = module.params

    ssid = p['ssid']
    validate_certs = p['validate_certs']

    api_usr = p['api_username']
    api_pwd = p['api_password']
    api_url = p['api_url']

    facts = dict()

    # fetch the list of drive objects
    try:
        (rc, resp) = request(api_url + "/storage-systems/%s/drives" % ssid,
                             headers=dict(Accept="application/json"),
                             url_username=api_usr, url_password=api_pwd, validate_certs=validate_certs)
    except:
        error = get_exception()
        module.fail_json(
            msg="Failed to obtain facts from storage array with id [%s]. Error [%s]" % (ssid, str(error)))

    # Define a counter using a composite key of the media type (ssd, hdd), spindle speed, and the capacity
    counter = collections.Counter(
        ["_".join([
            d['driveMediaType'], str(d['spindleSpeed']), str(int(int(d['rawCapacity'])/(1024*1024*1024)))
        ]) for d in resp]

    )
    facts['disks_by_type'] = [{'tag': key, 'count': counter[key], } for key in counter]

    result = dict(ansible_facts=facts, changed=False)
    module.exit_json(msg="Gathered facts for %s." % ssid, **result)


def request(url, data=None, headers=None, method='GET', use_proxy=True,
            force=False, last_mod_time=None, timeout=10, validate_certs=True,
            url_username=None, url_password=None, http_agent=None, force_basic_auth=True, ignore_errors=False):
    try:
        r = open_url(url=url, data=data, headers=headers, method=method, use_proxy=use_proxy,
                     force=force, last_mod_time=last_mod_time, timeout=timeout, validate_certs=validate_certs,
                     url_username=url_username, url_password=url_password, http_agent=http_agent,
                     force_basic_auth=force_basic_auth)
    except HTTPError:
        err = get_exception()
        r = err.fp

    try:
        raw_data = r.read()
        if raw_data:
            data = json.loads(raw_data)
        else:
            data = None
    except:
        if ignore_errors:
            pass
        else:
            raise

    resp_code = r.getcode()

    if resp_code >= 400 and not ignore_errors:
        raise Exception(resp_code, data)
    else:
        return resp_code, data


if __name__ == "__main__":
    main()
