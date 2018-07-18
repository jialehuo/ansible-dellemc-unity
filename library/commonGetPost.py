#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import supportive_functions
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'get': {
        'required': {'resource_type'},
        'optional': {'id', 'fields'}
    }
}

template = {
    constants.ACTIONS_KEY: {
        'get':
            {constants.EXECUTED_BY_SDK: 'get', constants.ACTION_TYPE_KEY: constants.ActionType.QUERY,
             constants.PARAMETER_TYPES_KEY:parameters_all.get('get')}
    }
}


def main():
    arguments = supportive_functions.create_arguments_for_ansible_module(template)

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    template[constants.REST_OBJECT_KEY] = ansible_module.params['get'].get('resource_type')
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
