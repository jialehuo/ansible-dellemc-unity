#!/usr/bin/python
def checkRequiredParameters(dictionaryOfParams, listOfRequired):
    for element in listOfRequired:
        if not dictionaryOfParams.get(element):
            return False
    return True


def checkOptionalParameters(dictionaryOfParams, listOfRequired, listOfOptional):
    for element in dictionaryOfParams.keys():
        if not ((element in listOfRequired) or (element in listOfOptional)):
            return False
    return True


def checkParameters(dictionaryOfParams, listOfRequired, listOfOptional):
    if not checkRequiredParameters(dictionaryOfParams, listOfRequired):
        return False
    return checkOptionalParameters(dictionaryOfParams, listOfRequired, listOfOptional)