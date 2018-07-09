#!/usr/bin/python

from ansible.module_utils.basic import *
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'create': {
        'VSA': {'required': {'name', 'addPoolUnitParameters'},
                'optional': {'description', 'alertThreshold', 'poolSpaceHarvestHighThreshold',
                             'poolSpaceHarvestLowThreshold', 'snapSpaceHarvestHighThreshold',
                             'snapSpaceHarvestLowThreshold', 'isHarvestEnabled',
                             'isSnapHarvestEnabled', 'isFASTCacheEnabled', 'isFASTVpScheduleEnabled',
                             'type'}}},
    'modify': {'VSA': {
        'required': {'id'},
        'optional': {'name', 'description', 'alertThreshold',
                     'poolSpaceHarvestHighThreshold',
                     'poolSpaceHarvestLowThreshold',
                     'snapSpaceHarvestHighThreshold', 'snapSpaceHarvestLowThreshold',
                     'isHarvestEnabled', 'isSnapHarvestEnabled', 'isFASTCacheEnabled',
                     'isFASTVpScheduleEnabled', 'addPoolUnitParameters'}
    }},
    'delete': {'required': {'id'}}
}


def _get_model(unity):
    reply = unity.query('system', {'fields': 'model'})
    return reply[0]['model']


def create(params, unity):
    params_types = parameters_all.get('create')
    model = _get_model(unity)
    if model == 'UnityVSA':
        reply = runner.do_update_request(unity, params, params_types.get('VSA'), 'pool', 'create')
        return reply
    else:
        raise TypeError("this model '" + model + "' is unsupported yet")


def modify(params, unity):
    model = _get_model(unity)
    params_types = parameters_all.get('modify')
    if model == "UnityVSA":
        reply = runner.do_update_request(unity, params, params_types.get('VSA'), 'pool', 'modify')
        return reply
    else:
        raise TypeError("this model '" + model + "' is unsupported yet")


template = {
    constants.REST_OBJECT_KEY: 'pool',
    constants.ACTIONS_KEY: {
        'create':
            {constants.EXECUTED_BY_KEY: create},
        'modify':
            {constants.EXECUTED_BY_KEY: modify},
        'delete':
            {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
             constants.PARAMETER_TYPES_KEY: parameters_all.get('delete')}
    }
}


def main():
    arguments = runner.create_arguments_for_ansible_module([
        {constants.ACTION_NAME: create}, {constants.ACTION_NAME: modify},
        {constants.ACTION_NAME: 'delete'}])

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
