# TODO: import important files

from dellemc_unity_sdk import validator
from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner

#a dict with req and opt params
def create(params, unity):
    repl = unity.query('system', {'fields': 'model'})
    model = repl['entries'][0]['model']
    model='UnityVSA'
    if model == 'UnityVSA':
        # TODO: how to output errors or some messages
        name = params['name']
        hostSP = params['hostSP']
        pool = params['pool']
        unity.update('create', 'nasServer',
                     {'name': name, 'hostSP': hostSP, 'pool': pool})
        return True, ''
    else:
        return False, 'this model' + model + 'unsupported yet'


def delete(params, unity):
    if 'id' not in params:
        return False, 'you must input id'
    nasServer_id = params['id']
    unity.update('delete', 'pool', {'id': nasServer_id})
    return True, ''


def main():
    runner.run([{"function":create},{"function":delete}])


if __name__ == '__main__':
    main()
