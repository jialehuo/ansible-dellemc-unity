#!/usr/bin/python
ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstableinterface'],
                    'supported_by': 'students'}
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import validator
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner

optional_list = {'tenant', 'isReplicationDestination', 'currentUnixDirectoryService', 
    'isMultiProtocolEnabled','allowUnmappedUser','defaultUnixUser','defaultWindowsUser',
    'isPacketReflectEnabled'}

def _exception_about_parameters(supported_parameters):
    return False, 'You did not input required parameters or inputted unsupported parameter, ' \
                  'supported parameters = ' + supported_parameters.__str__()


#a dict with req and opt params
def create(params, unity):
    
    required_list = {'name','hostSP','pool'}
    all_params = {'required': required_list,
                  'optional': optional_list}
    # TODO: how to output errors or some messages
    name = params['name']
    hostSP = params['hostSP']
    pool = params['pool']
    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    request_params = {'name': name, 'hostSP': hostSP, 'pool': pool}
            for parameter in optional_list:
            if params.get(parameter):
                request_params.update({parameter: params.get(parameter)})
    reply = unity.update('create', 'nasServer', request_params)
    return True, {'nasServer': {'id': reply['entries'][0]['id']}}



def delete(params, unity):
    all_params = {'required':'id'}
    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    if 'id' not in params:
        return False, 'you must input id'
    nasServer_id = params['id']
    unity.update('delete', 'nasServer', {'id': nasServer_id})
    return True, ''

def modify(params, unity):
    required_list = {'id'}
    optional_list.add('name') #TODO: we must not change global opt_list. figure out a workaround
    optional_list.add('homeSP')
    optional_list.add('pool')
        
        all_params = {'required': required_list, 'optional': optional_list}
        if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
        unity.update('modify', 'nasServer', params)
        return True, ''


def main():
    runner.run([{"function":create},{"function":delete},{"function":modify}])


if __name__ == '__main__':
    main()
