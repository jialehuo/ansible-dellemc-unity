from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import validator


# params_types = {'create': {''}}


def create(params, unity):
    optional_list = {'description', 'alertThreshold', 'poolSpaceHarvestHighThreshold', 'poolSpaceHarvestLowThreshold',
                     'snapSpaceHarvestHighThreshold', 'snapSpaceHarvestLowThreshold', 'isHarvestEnabled',
                     'isSnapHarvestEnabled', 'isFASTCacheEnabled', 'isFASTVpScheduleEnabled', 'type',
                     }
    repl = unity.query('system', {'fields': 'model'})
    model = repl['entries'][0]['model']
    if model == 'UnityVSA':
        params_types = {'required': {'name', 'addPoolUnitParameters'},
                        'optional': optional_list}
        # if not validator.check_parameters(params, params_types):
        #    return False, 'You did not input required parameters or inputted unsupported parameter, ' \
        #                  'supported parameters = ' + params_types.__str__()
        name = params['name']
        addPoolUniParameters = params['addPoolUnitParameters']
        request_params = {'name': name, 'addPoolUnitParameters': addPoolUniParameters}
        #for parameter in optional_list:
        #    if params.get(parameter):
        #        request_params.update({parameter: params.get(parameter)})
        unity.update('create', 'pool', request_params)
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
    runner.run([{'function': create}, {'function': delete}])


if __name__ == '__main__':
    main()
