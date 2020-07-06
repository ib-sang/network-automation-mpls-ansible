#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}



import traceback
import xml.dom.minidom

try:
    import ncclient.manager
    HAS_NCCLIENT = True
except ImportError:
    HAS_NCCLIENT = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native



def netconf_edit_config(m, xml, commit, retkwargs, datastore):
    m.lock(target=datastore)
    try:
        if datastore == "candidate":
            m.discard_changes()
        #config_before = m.get_config(source=datastore)
        m.edit_config(target=datastore, config=xml)
        #config_after = m.get_config(source=datastore)
        #changed = config_before.data_xml != config_after.data_xml
        #if changed and commit and datastore == "candidate":
        #    if ":confirmed-commit" in m.server_capabilities:
        #        m.commit(confirmed=True)
        #        m.commit()
        #    else:
        #        m.commit()
        return False
    finally:
        m.unlock(target=datastore)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            port=dict(type='int', default=830),
            hostkey_verify=dict(type='bool', default=True),
            allow_agent=dict(type='bool', default=True),
            look_for_keys=dict(type='bool', default=True),
            datastore=dict(choices=['auto', 'candidate', 'running'], default='auto'),
            save=dict(type='bool', default=False),
            username=dict(type='str', required=True, no_log=True),
            password=dict(type='str', required=True, no_log=True),
            xml=dict(type='str', required=False),
            src=dict(type='path', required=False),
            timeout=dict(type='int', required=False, default=120),
        ),
        mutually_exclusive=[('xml', 'src')]
    )




if __name__ == '__main__':
    main()