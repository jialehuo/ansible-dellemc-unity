#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import constants

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstable'],
                    'supported_by': 'community'}

parameters_all = {
    'create': {
        'required': {'srcResourceId', 'dstResourceId', 'maxTimeOutOfSync'},
        'optional': {'remoteSystem', 'srcSPAInterface', 'srcSPBInterface', 'dstSPAInterface',
                     'dstSPBInterface', 'autoInitiate', 'name', 'members', 'hourlySnapReplicationPolicy',
                     'dailySnapReplicationPolicy', 'replicateExistingSnaps'},
    },
    'modify': {
        'required': {'id'},
        'optional': {'maxTimeOutOfSync', 'name', 'srcSPAInterface', 'srcSPBInterface', 'dstSPAInterface',
                     'dstSPBInterface', 'hourlySnapReplicationPolicy', 'dailySnapReplicationPolicy'},
    },
    'delete': {'required': {'id'}},
    'resume': {
        'required': {'id'},
        'optional': {'srcSPAInterface', 'srcSPBInterface', 'dstSPAInterface', 'dstSPBInterface', 'forceFullCopy'}
    },
    'pause': {'required': {'id'}},
    'sync': {'required': {'id'}},
    'failover': {'required': {'id'},
                 'optional': {'sync'}},
    'failback': {'required': {'id'},
                 'optional': {'forceFullCopy'}}
}


def resume(params, unity):
    reply = runner.do_update_request(unity, params, parameters_all['resume'], 'replicationSession', 'resume')
    return reply


def pause(params, unity):
    reply = runner.do_update_request(unity, params, parameters_all['pause'], 'replicationSession', 'pause')
    return reply


def sync(params, unity):
    reply = runner.do_update_request(unity, params, parameters_all['sync'], 'replicationSession', 'sync')
    return reply


def failover(params, unity):
    reply = runner.do_update_request(unity, params, parameters_all['failover'], 'replicationSession', 'failover')
    return reply


def failback(params, unity):
    reply = runner.do_update_request(unity, params, parameters_all['failback'], 'replicationSession', 'failback')
    return reply


template = {
    constants.REST_OBJECT_KEY: 'replicationSession',
    constants.ACTIONS_KEY: {
        'create': {constants.ACTION_TYPE: constants.ActionType.UPDATE,
                   constants.PARAMETER_TYPES_KEY: parameters_all.get('create')},
        'modify': {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                   constants.PARAMETER_TYPES_KEY: parameters_all.get('modify')},
        'delete': {constants.ACTION_TYPE_KEY: constants.ActionType.UPDATE,
                   constants.PARAMETER_TYPES_KEY: parameters_all.get('delete')},
        'resume': {constants.EXECUTED_BY: resume},
        'pause': {constants.EXECUTED_BY: pause},
        'sync': {constants.EXECUTED_BY: sync},
        'failover': {constants.EXECUTED_BY: failover},
        'failback': {constants.EXECUTED_BY: failback}
    }
}


def main():
    arguments = runner.create_arguments_for_ansible_module(template)

    ansible_module = AnsibleModule(arguments, supports_check_mode=True)
    runner.run(ansible_module, template)


if __name__ == '__main__':
    main()
