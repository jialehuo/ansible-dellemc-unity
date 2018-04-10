def checkRequiredParameters(dictionaryOfParams,listOfRequired ):
    for element in listOfRequired:
        if not dictionaryOfParams[element]:
            return False
    return True

def checkOptionalParametrs(dictionaryOfParams, listOfRequired, listOfOptional):
    for element in dictionaryOfParams.keys():
        if (not element in listOfRequired) and (not element in listOfOptional):
            return False
    return True

def checkParameters(dictionaryOfParams, listOfRequired, listOfOptional):

    if not checkRequiredParameters(dictionaryOfParams, listOfRequired):
        return False
    return checkOptionalParametrs(dictionaryOfParams, listOfRequired, listOfOptional)
