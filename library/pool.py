#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

from dellemc_unity_sdk import runner
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'createVSA': {
        'required': {'name', 'addPoolUnitParameters'},
        'optional': {'description', 'alertThreshold', 'poolSpaceHarvestHighThreshold',
                     'poolSpaceHarvestLowThreshold', 'snapSpaceHarvestHighThreshold',
                     'snapSpaceHarvestLowThreshold', 'isHarvestEnabled',
                     'isSnapHarvestEnabled', 'isFASTCacheEnabled', 'isFASTVpScheduleEnabled',
                     'type'}},
    'modifyVSA': {
        'required': {'id'},
        'optional': {'name', 'description', 'alertThreshold',
                     'poolSpaceHarvestHighThreshold',
                     'poolSpaceHarvestLowThreshold',
                     'snapSpaceHarvestHighThreshold', 'snapSpaceHarvestLowThreshold',
                     'isHarvestEnabled', 'isSnapHarvestEnabled', 'isFASTCacheEnabled',
                     'isFASTVpScheduleEnabled', 'addPoolUnitParameters'}
    },
    'delete': {'required': {'id'}}
}

template = {
    constants.REST_OBJECT_KEY: 'pool',
    constants.ACTIONS_KEY: {
        'createVSA':
            {
                constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                constants.PARAMETER_TYPES_KEY: parameters_all.get('createVSA'),
                constants.DO_ACTION: 'create'
            },
        'modifyVSA':
            {
                constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                constants.PARAMETER_TYPES_KEY: parameters_all.get('modifyVSA'),
                constants.DO_ACTION: 'modify'
            },
        'delete':
            {
                constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                constants.PARAMETER_TYPES_KEY: parameters_all.get('delete')
            }
    }
}


def main():
    arguments = runner.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: 'createVSA'},
        {constants.ACTION_NAME: 'modifyVSA'},
        {constants.ACTION_NAME: 'delete'}
    ])

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
