#!/usr/bin/python

from ansible.module_utils.basic import *
from dellemc_unity_sdk import runner
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
    constants.REST_OBJECT_KEY: 'fileInterface',
    constants.ACTIONS_KEY: {
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
    arguments = runner.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: 'create'},
        {constants.ACTION_NAME: 'modify'},
        {constants.ACTION_NAME: 'delete'}])

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
