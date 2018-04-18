# TODO: import important files

from ansible.module_utils.dellemc_unity import common_functions
from ansible.module_utils.dellemc_unity.unity import Unity
from ansible.module_utils.dellemc_unity import module
from ansible.module_utils.dellemc_unity.ansible_function import AnsibleFunction


def create(params, unity):
    repl = unity.query('system', {'fields': 'model'})
    model = repl['entries'][0]['model']
    if model == 'UnityVSA':
        # TODO: how to output errors or some messages
        name = params['name']
        addPoolUniParameters = params['addPoolUnitParameters']
        unity.update('create', 'pool',
                     {'name': name, 'addPoolUnitParameters': addPoolUniParameters})
        return True, ''
    else:
        return False, 'this model' + model + 'unsupported yet'


def delete(params, unity):
    if id not in params:
        return False, 'you must input id'
    pool_id = params['id']
    unity.update('delete', 'pool', {'id': pool_id})
    return True, ''


def main():
    module.run([AnsibleFunction('create', create), AnsibleFunction('delete', delete)])


if __name__ == '__main__':
    main()
