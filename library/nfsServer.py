#!/usr/bin/python
ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['unstableinterface'],
                    'supported_by': 'students'}
from ansible.module_utils.basic import AnsibleModule
from dellemc_unity_sdk import validator
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner
import json
optional_list = {'hostName','nfsv4Enabled','isSecureEnabled','kdcType','kdcUsername','kdcPassword',
'isExtendedCredentialsEnabled','credentialsCacheTTL'}

def _exception_about_parameters(supported_parameters):
    return False, 'You did not input required parameters or inputted unsupported parameter, ' \
                  'supported parameters = ' + supported_parameters.__str__()


def _get_message_from_update(resp_from_request):
  result = {}
  if resp_from_request and resp_from_request.text:
    dictionary = json.loads(resp_from_request.text)
    result=dictionary.get('content')
  return result

#a dict with req and opt params
def create(params, unity):
    
    required_list = {'nasServer'}
    all_params = {'required': required_list,
                  'optional': optional_list}
    # TODO: how to output errors or some messages
    nasServer = params.get('nasServer')

    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    request_params = {'nasServer': nasServer}
    for parameter in optional_list:
        if params.get(parameter):
            request_params.update({parameter: params.get(parameter)})
    reply = unity.update('create', 'nfsServer', request_params)
    cont = _get_message_from_update(reply)
    return True, cont
    #id
    #reply
    #{'nfsServer': {'id': reply['entries'][0]['id']}}

def delete(params, unity):
    all_params = {'required': {'id'}}
    repl = unity.query('nasServer', {'fields': 'id'})
    if not validator.check_parameters(params, all_params):
            return _exception_about_parameters(all_params)
    if 'id' not in params:
        return False, 'you must input id'
    nfsServer_id = params['id']
    reply = unity.update('delete', 'nfsServer', {'id': nfsServer_id})
    return True, ''
    #reply

def modify(params, unity):
    required_list = {'id'}
    optional_list.add('nfsServer') #TODO: we must not change global opt_list. figure out a workaround

    all_params = {'required': required_list, 'optional': optional_list}
    if not validator.check_parameters(params, all_params):
        return _exception_about_parameters(all_params)
    unity.update('modify', 'nfsServer', params)
    return True, ''


def main():
    runner.run([{"function":create},{"function":delete},{"function":modify}])


if __name__ == '__main__':
    main()
