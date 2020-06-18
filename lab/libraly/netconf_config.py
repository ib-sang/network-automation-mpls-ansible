#!/usr/bin/python

# (c) 2020, Ib Baba Sangaré < project PFE >
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

    if not HAS_NCCLIENT:
        module.fail_json(msg='could not import the python library '
                         'ncclient required by this module')

    if (module.params['src']):
        config_xml = str(module.params['src'])
    elif module.params['xml']:
        config_xml = str(module.params['xml'])
    else:
        module.fail_json(msg='Option src or xml must be provided')

    try:
        xml.dom.minidom.parseString(config_xml)

    except Exception as e:
        module.fail_json(msg='error parsing XML: %s' % to_native(e), exception=traceback.format_exc())

    nckwargs = dict(
        host=module.params['host'],
        port=module.params['port'],
        hostkey_verify=module.params['hostkey_verify'],
        allow_agent=module.params['allow_agent'],
        look_for_keys=module.params['look_for_keys'],
        username=module.params['username'],
        password=module.params['password'],
        timeout=module.params['timeout'],
    )

    try:
        m = ncclient.manager.connect(**nckwargs)
    except ncclient.transport.errors.AuthenticationError:
        module.fail_json(
            msg='authentication failed while connecting to device'
        )
    except Exception as e:
        module.fail_json(msg='error connecting to the device: %s' % to_native(e), exception=traceback.format_exc())

    retkwargs = dict()
    retkwargs['server_capabilities'] = list(m.server_capabilities)

    if module.params['datastore'] == 'candidate':
        if ':candidate' in m.server_capabilities:
            datastore = 'candidate'
        else:
            m.close_session()
            module.fail_json(
                msg=':candidate is not supported by this netconf server'
            )
    elif module.params['datastore'] == 'running':
        if ':writable-running' in m.server_capabilities:
            datastore = 'running'
        else:
            m.close_session()
            module.fail_json(
                msg=':writable-running is not supported by this netconf server'
            )
    elif module.params['datastore'] == 'auto':
        if ':candidate' in m.server_capabilities:
            datastore = 'candidate'
        elif ':writable-running' in m.server_capabilities:
            datastore = 'running'
        else:
            m.close_session()
            module.fail_json(
                msg='neither :candidate nor :writable-running are supported by this netconf server'
            )
    else:
        m.close_session()
        module.fail_json(
            msg=module.params['datastore'] + ' datastore is not supported by this ansible module'
        )

    if module.params['save']:
        if ':startup' not in m.server_capabilities:
            module.fail_json(
                msg='cannot copy <running/> to <startup/>, while :startup is not supported'
            )

    try:
        changed = netconf_edit_config(
            m=m,
            xml=config_xml,
            commit=True,
            retkwargs=retkwargs,
            datastore=datastore,
        )
        if changed and module.params['save']:
            m.copy_config(source="running", target="startup")
    except Exception as e:
        module.fail_json(msg='error editing configuration: %s' % to_native(e), exception=traceback.format_exc())
    finally:
        m.close_session()

    module.exit_json(changed=changed, **retkwargs)


if __name__ == '__main__':
    main()