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
        'name': dict(required=True, type='str'),
        'fsParameters': dict(required=True),
        'description': dict(type='str'),
        'replicationParameters': dict(type='dict'),
        'snapScheduleParameters': dict(type='dict'),
        'cifsFsParameters': dict(type='dict'),
        'nfsShareCreate': dict(type='array'),
        'cifsShareCreate': dict(type='array')
    }
}

template = {
    constants.REST_OBJECT_KEY: 'storageResource',
    constants.ACTIONS_KEY: {
        'create': {
            constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
            constants.PARAMETER_TYPES_KEY: parameters_all.get('create'),
            constants.DO_ACTION: 'createFilesystem'
        }
    }
}


def main():
    arguments = supportive_functions.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: 'create'}
    ])
    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
