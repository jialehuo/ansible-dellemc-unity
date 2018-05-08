
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import validator


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
    if 'id' not in params:
        return False, 'you must input id'
    pool_id = params['id']
    unity.update('delete', 'pool', {'id': pool_id})
    return True, ''


def main():
    runner.run([{'function':create}, {'function':delete}])


if __name__ == '__main__':
    main()
