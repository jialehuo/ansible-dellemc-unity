#!/usr/bin/python
ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstableinterface'],
                    'supported_by': 'students'}
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import validator
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner

optional_list = {
    'netmask','v6PrefixLength','gateway',
    'vlanId','isPreferred','role'}

def _exception_about_parameters(supported_parameters):
    return False, 'You did not input required parameters or inputted unsupported parameter, ' \
                  'supported parameters = ' + supported_parameters.__str__()


#a dict with req and opt params
def create(params, unity):
    
    required_list = {'nasServer','ipPort','ipAddress'}
    all_params = {'required': required_list,
                  'optional': optional_list}
    # TODO: how to output errors or some messages
    nasServer = params['nasServer'] #TODO: required_list[0]
    ipPort = params ['ipPort']
    ipAddress = params ['ipAddress']
    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    request_params = {'nasServer': nasServer, 'ipPort': ipPort, 'ipAddress': ipAddress}
            for parameter in optional_list:
            if params.get(parameter):
                request_params.update({parameter: params.get(parameter)})
    reply = unity.update('create', 'fileInterface', request_params)
    return True, {'fileInterface': {'id': reply['entries'][0]['id']}}

def delete(params, unity):
    all_params = {'required':'id'}
    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    if 'id' not in params:
        return False, 'you must input id'
    fileInterface_id = params['id']
    unity.update('delete', 'fileInterface', {'id': fileInterface_id})
    return True, ''

def modify(params, unity):
    required_list = {'id'}
    optional_list.add('nasServer') #TODO: we must not change global opt_list. figure out a workaround
    optional_list.add('ipPort')
    optional_list.add('ipAddress')
        all_params = {'required': required_list, 'optional': optional_list}
        if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
        unity.update('modify', 'fileInterface', params)
        return True, ''


def main():
    runner.run([{"function":create},{"function":delete},{"function":modify}])


if __name__ == '__main__':
    main()
