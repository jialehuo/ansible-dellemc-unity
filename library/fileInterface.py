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
        'required': {'nasServer','ipPort','ipAddress'},
        'optional': {'netmask','v6PrefixLength','gateway','vlanId','isPreferred','role'},
        },
    'modify': {
        'required': {'id'},
        'optional': {'nasServer','ipPort','ipAddress','netmask','v6PrefixLength','gateway','vlanId','isPreferred','role'},
        },
    'delete': {'required': {'id'}}
}

template = {
    constants.REST_OBJECT: 'fileInterface',
    constants.ACTIONS: {
        'create': 
        {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
            constants.PARAMETER_TYPES_KEY:parameters_all.get('create')},
        'modify': 
        {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
            constants.PARAMETER_TYPES_KEY:parameters_all.get('modify')},
        'delete': 
        {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
            constants.PARAMETER_TYPES_KEY:parameters_all.get('delete')}
    }
}


def main():
    arguments = supportive_functions.create_arguments_for_ansible_module(template)

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
