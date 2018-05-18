from ansible.module_utils.basic import AnsibleModule
import sys, os

sys.path.append('/home/ansible/Vadim/new/my_sdk/dellemc-unity-sdk/dellemc-unity-sdk')

from dellemc_unity import Unity
from common_functions import refactor_params


class Iscsi(Unity):

    def __init__(self, module):
        super(Iscsi,self).__init__(module)
        self.params = module.params
        self.create_spec = {
            'ethernetPort': {'default': None, 'required': True, 'type': 'dict'},
            'ipAddress': {'default': None, 'required': True, 'type': 'str'},
            'netmask': {'default': '255.255.255.0', 'required': True, 'type': 'str'}
        }
        self.update_spec = {}
        self.delete_spec = {'id': {'default': None, 'required': True, 'type': 'str'}}

    def create(self, data):
        data = refactor_params(self.create_spec, data)
        data['resource_type'] = 'iscsiPortal'
        self.runUpdate(data)

    def delete(self, data):
        data = refactor_params(self.delete_spec, data)
        data['resource_type'] = 'iscsiPortal'
        data['action'] = 'delete'
        self.runUpdate(data)

    def _start_create(self):
        params = self.params['create'][0]
        if 'interfaces' in params:
            for key in params:
                self.create(params[key])
        else:
            self.create(params)

    def _start_delete(self):
        params = self.params['delete'][0]
        if 'interfaces' in params:
            for key in params:
                self.delete(params[key])
        else:
            self.create(params)

    def run(self):
        self.startSession()
        if self.params['create']:
            self._start_create()
        if self.params['delete']:
            self._start_delete()
        if self.params['update']:
            self._start_create()

        self.stopSession()


def main():
    argument_spec = dict(
        unity_hostname=dict(default=None, required=True, type='str'),
        unity_username=dict(default='admin', type='str'),
        unity_password=dict(default='Password123#', type='str'),
        unity_license_path=dict(default=None, type='path'),
        unity_password_updates=dict(default=None, type='list'),
        create=dict(default=None, required=False, type='list'),
        delete=dict(default=None, required=False, type='list'),
        update=dict(default=None, required=False, type='list')
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    unity = Iscsi(module)
	
    #module.fail_json(msg=module.params['create'][0])
    unity.run()
    if unity.err:
        unity.exitFail()
    else:
        unity.exitSuccess()


if __name__ == '__main__':
    main()
