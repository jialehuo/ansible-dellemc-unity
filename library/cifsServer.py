#!/usr/bin/python
from ansible.module_utils.basic import *
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import supportive_functions
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'create': {
        'nasServer': dict(required=True, type='dict'),
        'name': dict(type='str'),
        'description': dict(type='str')
    }
}

template = {
    constants.REST_OBJECT_KEY: 'cifsServer',
    constants.ACTIONS_KEY: {}
}


def main():
    arguments = supportive_functions.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: 'create'}
    ])
    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
