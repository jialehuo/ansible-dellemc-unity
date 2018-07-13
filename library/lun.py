#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import validator
from dellemc_unity_sdk import supportive_functions
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'create': {
        'required': {'name', 'lunParameters'},
        'optional': {'description','replicationParameters','snapScheduleParameters'},
        },
    'modify': {
        'required': {'id'},
        'optional': {'name','description','replicationParameters','snapScheduleParameters','lunParameters'},
        },
    'delete': {'required': {'id'}}
}

template = {
    constants.REST_OBJECT_KEY: 'storageResource',
    constants.ACTIONS_KEY: {
        'createLun': {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
        constants.PARAMETER_TYPES_KEY:parameters_all.get('create')},
        'modifyLun': {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
        constants.PARAMETER_TYPES_KEY:parameters_all.get('modify')},
        'delete': {constants.ACTION_TYPE_KEY:constants.ActionType.UPDATE, 
        constants.PARAMETER_TYPES_KEY:parameters_all.get('delete')}
    }
}


def main():
    arguments = runner.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: 'createLun'},{constants.ACTION_NAME: 'modifyLun'},
        {constants.ACTION_NAME: 'delete'}])

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
