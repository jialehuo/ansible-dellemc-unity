from ansible.module_utils.dellemc_unity import validator
from ansible.module_utils.dellemc_unity.unity import Unity
from ansible.module_utils.dellemc_unity import runner
from ansible.module_utils.dellemc_unity.ansible_function import AnsibleFunction


def create(params, unity):
    unity.update('create', 'iscsiPortal',
                 {"ethernetPort": params["ethernetPort"],
                  "ipAddress": params["ipAddress"],
                  "netmask": params["netmask"]})
    return True, ''


def delete(params, unity):
    if 'id' not in params:
        return False, 'you must input id'
    iscsi_id = params['id']
    unity.update('delete', 'iscsiPortal', {'id': iscsi_id})
    return True, ''


def check(params, unity):
    if 'id' not in params['fields']:
        return False, 'you must input id'
    unity.query('iscsiPortal', params['fields'])
    return True, ''


if __name__ == '__main__':
    run(validator('create', create), validator('delete', delete))
