from dellemc_unity_sdk.unity import Unity
from dellemc_unity_sdk import runner
from dellemc_unity_sdk import validator


# params_types = {'create': {''}}


def _get_model(unity):
    repl = unity.query('system', {'fields': 'model'})
    return repl['entries'][0]['model']


def _exception_about_parameters(supported_parameters):
    return False, 'You did not input required parameters or inputted unsupported parameter, ' \
                  'supported parameters = ' + supported_parameters.__str__()


def create(params, unity):
    optional_list = {'description', 'alertThreshold', 'poolSpaceHarvestHighThreshold', 'poolSpaceHarvestLowThreshold',
                     'snapSpaceHarvestHighThreshold', 'snapSpaceHarvestLowThreshold', 'isHarvestEnabled',
                     'isSnapHarvestEnabled', 'isFASTCacheEnabled', 'isFASTVpScheduleEnabled', 'type'
                     }
    model = _get_model(unity)
    if model == 'UnityVSA':
        params_types = {'required': {'name', 'addPoolUnitParameters'},
                        'optional': optional_list}
        if not validator.check_parameters(params, params_types):
            return _exception_about_parameters(params_types)
        name = params['name']
        addPoolUniParameters = params['addPoolUnitParameters']
        request_params = {'name': name, 'addPoolUnitParameters': addPoolUniParameters}
        for parameter in optional_list:
            if params.get(parameter):
                request_params.update({parameter: params.get(parameter)})
        reply = unity.update('create', 'pool', request_params)
        return True, {'pool': {'id': reply['entries'][0]['id']}}
    else:
        return False, 'this model' + model + 'unsupported yet'


def delete(params, unity):
    params_type = {'required': {'id'}}
    if not validator.check_parameters(params, params_type):
        return _exception_about_parameters(params_type)
    if 'id' not in params:
        return False, 'you must input id'
    pool_id = params['id']
    unity.update('delete', 'pool', {'id': pool_id})
    return True, ''


def modify(params, unity):
    required_params = {'id'}
    optional_list = {'name', 'description', 'alertThreshold', 'poolSpaceHarvestHighThreshold', 'poolSpaceHarvestLowThreshold',
                     'snapSpaceHarvestHighThreshold', 'snapSpaceHarvestLowThreshold', 'isHarvestEnabled',
                     'isSnapHarvestEnabled', 'isFASTCacheEnabled', 'isFASTVpScheduleEnabled'
                     }
    model = _get_model(unity)
    if model == "UnityVSA":
        optional_list.add('addPoolUnitParameters')
        parameters_types = {'required': required_params, 'optional': optional_list}
        if not validator.check_parameters(params, parameters_types):
            return _exception_about_parameters(parameters_types)
        unity.update('modify', 'pool', params)
        return True, ''
    else:
        return False, 'this model ' + model + ' unsupported yet'


def main():
    runner.run([{'function': create}, {'function': modify}, {'function': delete}])


if __name__ == '__main__':
    main()
