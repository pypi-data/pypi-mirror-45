# coding=utf-8
# import
from copy import copy
from json import dumps, loads
from pythoncommontools.objectUtil.objectUtil import EncryptionMarkup, dumpObjetToDict, loadObjectFromDict
# convert a dictionary into an JSON dictionary
def convertObjectToJsonDict(objectToConvert):
    '''
    convert to JSON native
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    '''
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToConvert)
        objectJsonDict = convertObjectToJsonDict(objectDict)
        pass
    elif type(objectToConvert) == complex:
        objectJsonDict = str(objectToConvert)
        pass
    elif type(objectToConvert) in {memoryview, bytes, bytearray}:
        objectJsonDict = list(objectToConvert)
        pass
    elif type(objectToConvert) in {list, tuple, set, frozenset, range}:
        objectJsonDict = [convertObjectToJsonDict(_) for _ in objectToConvert]
        pass
    elif type(objectToConvert) == dict:
        objectJsonDict = {}
        for oldKey,oldValue in objectToConvert.items():
            newKey = convertObjectToJsonDict(oldKey)
            newKey = str(newKey)
            newValue = convertObjectToJsonDict(oldValue)
            objectJsonDict[newKey] = newValue
    else:
        # INFO : shallow copy to avoid modifying original object
        objectJsonDict = copy(objectToConvert)
    # return dict
    return objectJsonDict
# dump dictionary to JSON
def dumpObjectToSimpleJson(objectToDump):
    # copy & adapt data to dump
    objectJsonDict = convertObjectToJsonDict(objectToDump)
    # dump & return
    dumpedJson = dumps(objectJsonDict)
    return dumpedJson
def loadObjectFromSimpleJson(json):
    dictToLoad = loads(json)
    instantiatedObject = loadObjectFromDict(dictToLoad)
    return instantiatedObject
pass
