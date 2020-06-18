#!/usr/bin/python

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
    print('hello word')
    
if __name__ == '__main__':
    main()