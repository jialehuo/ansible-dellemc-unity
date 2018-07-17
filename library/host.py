#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import supportive_functions
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'create': {
        'required': {'type', 'name'},
        'optional': {'description','osType','tenant'},
        },
    'modify': {
        'required': {'id'},
        'optional': {'name','description','osType'},
        },
    'delete': {'required': {'id'}}
}

template = {
    constants.REST_OBJECT: 'host',
    constants.ACTIONS: {
        'create': {constants.ACTION_TYPE:constants.ActionType.UPDATE,
        constants.PARAMETER_TYPES:parameters_all.get('create')},
        'modify': {constants.ACTION_TYPE:constants.ActionType.UPDATE,
        constants.PARAMETER_TYPES:parameters_all.get('modify')},
        'delete': {constants.ACTION_TYPE:constants.ActionType.UPDATE,
        constants.PARAMETER_TYPES:parameters_all.get('delete')}
    }
}


def main():
    arguments = supportive_functions.create_arguments_for_ansible_module(template)

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
