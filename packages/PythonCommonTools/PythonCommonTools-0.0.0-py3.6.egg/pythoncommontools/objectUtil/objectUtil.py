# coding=utf-8
# import
from hashlib import sha512
from sys import byteorder
from collections import OrderedDict
from enum import Enum , unique
from importlib import import_module
from copy import copy
# global initialization
@unique
class EncryptionMarkup(Enum):
    DICT = "__dict__"
    CLASS_NAME = "className"
    MODULE = "module"
# common functions
# convert an object into a dictionary
def dumpObjetToDict(objectToDump):
    # extract dict from object (if possible)
    '''INFO :
     - 'memoryview' object is a special one, without __dict__ attribut
       see : https://docs.python.org/3.3/library/stdtypes.html#memoryview
     - convert iterators elements (list,tuple,set,frozenset,dict)
     - some specific objects (i.e datetime.datetime) does not have __dict__ propertie
       so they can not be dumped to dictionnary or JSON
       so we finally use string to dump
    '''
    objectType = type(objectToDump)
    if hasattr(objectToDump, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToDump.__dict__)
        # add type data
        if hasattr(objectToDump,"__class__") and hasattr(objectToDump,"__module__"):
            objectDict[EncryptionMarkup.CLASS_NAME.value] = objectToDump.__class__.__name__
            objectDict[EncryptionMarkup.MODULE.value] = objectToDump.__module__
    elif objectType==memoryview:
        objectDict = objectToDump.tobytes()
        pass
    elif objectType == list:
        objectDict = [dumpObjetToDict(_) for _ in objectToDump]
        pass
    elif objectType == tuple:
        objectDict = [dumpObjetToDict(_) for _ in objectToDump]
        objectDict = tuple(objectDict)
        pass
    elif objectType == set:
        objectDict = [dumpObjetToDict(_) for _ in objectToDump]
        objectDict = set(objectDict)
        pass
    elif objectType == frozenset:
        objectDict = [dumpObjetToDict(_) for _ in objectToDump]
        objectDict = frozenset(objectDict)
        pass
    elif objectType == dict:
        objectDict = {}
        for key, value in objectToDump.items():
            newKey = dumpObjetToDict(key)
            newValue = dumpObjetToDict(value)
            objectDict[newKey] = newValue
        pass
    elif objectToDump and objectType not in {bool,int,float,complex,range,str,bytes,bytearray}:
        objectDict = str(objectToDump)
    else:
        # INFO : shallow copy to avoid modifying original object
        objectDict = copy(objectToDump)
    # return dict
    return objectDict
# load object from a dictionary
def loadObjectFromDict(baseDict):
    # assume baseDict is not really a dict
    # INFO : shallow copy to avoid modifying original object
    baseType = type(baseDict)
    instantiatedObject = copy(baseDict)
    if baseType == list:
        instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
        pass
    elif baseType == tuple:
        instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
        instantiatedObject = tuple(instantiatedObject)
        pass
    elif baseType == set:
        instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
        instantiatedObject = set(instantiatedObject)
        pass
    elif baseType == frozenset:
        instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
        instantiatedObject = frozenset(instantiatedObject)
        pass
    elif baseType == dict:
        instantiatedObject = {}
        # continue loading deeper
        for key, value in baseDict.items():
            instantiatedObject[key] = loadObjectFromDict(value)
        # load explicit object
        if EncryptionMarkup.CLASS_NAME.value in baseDict and EncryptionMarkup.MODULE.value in baseDict:
            # INFO : shallow copy to avoid modifying original object
            attributs = copy(instantiatedObject)
            # invoke target object
            importedModule = import_module(baseDict[EncryptionMarkup.MODULE.value])
            loadedClass = getattr(importedModule, baseDict[EncryptionMarkup.CLASS_NAME.value])
            instantiatedObject = loadedClass()
            # update attributes
            instantiatedObject.__dict__.update(attributs)
            # clean encryption markups (if present)
            if hasattr(instantiatedObject, EncryptionMarkup.MODULE.value):
                delattr(instantiatedObject, EncryptionMarkup.MODULE.value)
            if hasattr(instantiatedObject, EncryptionMarkup.CLASS_NAME.value):
                delattr(instantiatedObject, EncryptionMarkup.CLASS_NAME.value)
        # return object
    return instantiatedObject
# get string representation of an object
def objectStringRepresentation(objectToStr):
    objectDict = dumpObjetToDict(objectToStr)
    objectStr = str(objectDict)
    return objectStr
# convert a dictionary into an ORDERED dictionary
def convertObjectToOrderedDict(objectToConvert):
    # assume dict is already ordered
    # INFO : can not copy object because it can contains memory view in deeper levels
    objectType = type(objectToConvert)
    objectOrderedDict = objectToConvert
    # extract dict from object (if possible)
    #INFO : convert iterators elements (list,tuple,set,frozenset,dict)
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToConvert)
        objectOrderedDict = convertObjectToOrderedDict(objectDict)
        pass
    elif objectType == memoryview:
        objectOrderedDict = objectToConvert.tobytes()
        pass
    elif objectType in {list,tuple,set,frozenset}:
        objectOrderedDict = [convertObjectToOrderedDict(_) for _ in objectToConvert]
        # INFO : all data must be of same type for sorting
        objectOrderedDict = [str(_) for _ in objectOrderedDict]
        objectOrderedDict.sort()
        objectOrderedDict = tuple(objectOrderedDict)
        pass
    elif objectType == dict:
        # store data with string key
        stringKeyDict = {}
        for oldKey,oldValue in objectToConvert.items():
            orderedKey = convertObjectToOrderedDict(oldKey)
            stringKey = str(orderedKey)
            orderedValue = convertObjectToOrderedDict(oldValue)
            stringKeyDict[stringKey] = orderedValue
        # ordered string keys
        orderedStringKeys = convertObjectToOrderedDict(stringKeyDict.keys())
        # fill ordered dict
        objectOrderedDict = OrderedDict()
        for orderedKey in orderedStringKeys:
            objectOrderedDict[orderedKey] = stringKeyDict[orderedKey]
        pass
    # return dict
    return objectOrderedDict
# compute object hash
def objectHash(objectToHash):
    # INFO : object must be ordered to have the same string representation
    objectOrderedDict = convertObjectToOrderedDict(objectToHash)
    hashAlgorithm = sha512()
    hashAlgorithm.update(str(objectOrderedDict).encode())
    digest = hashAlgorithm.digest()
    hash = int.from_bytes(digest, byteorder=byteorder, signed=False)
    return hash
# compare 2 objects
def objectComparison(originalObject, modelObject):
    '''INFO :
     - normally, in python 0.==0 even if type(0.)!=type(0)
       however, for consistency and stability, we will ensure types are equals
     - convert iterators elements (list,tuple,set,frozenset,dict)
       furthermore, python can have issues with multi dimensional arrays : The truth value of an array with more than one element is ambiguous
       so we adapt comparison method
     '''
    comparison = False
    if type(originalObject) == type(modelObject):
        # dump to dict
        originalDict = dumpObjetToDict(originalObject)
        modelDict = dumpObjetToDict(modelObject)
        # compare deeper
        if type(originalDict) == dict:
            originalKeys = tuple(originalDict.keys())
            modelKeys = tuple(modelDict.keys())
            comparison = objectComparison(originalKeys, modelKeys)
            if comparison:
                for key,originalValue in originalDict.items():
                    modelValue = modelDict[key]
                    comparison = objectComparison(originalValue, modelValue)
                    if not comparison:
                        break
                    pass
                pass
            pass
        if type(originalDict) in {list,tuple}:
            comparison = len(originalDict)==len(modelDict)
            if comparison:
                for index, originalElement in enumerate(originalDict):
                    modelElement = modelDict[index]
                    comparison = objectComparison(originalElement, modelElement)
                    if not comparison:
                        break
                    pass
                pass
            pass
        elif type(originalDict) in {set,frozenset}:
            comparison = len(originalDict)==len(modelDict)
            if comparison:
                for originalElement in originalDict:
                    comparison = originalElement in modelDict
                    if not comparison:
                        break
                    pass
                pass
            pass
        else :
            comparison = originalDict == modelDict
        pass
    return comparison
# get string representation of a function/method arguments
def methodArgsStringRepresentation(parametersList , localValuesDict):
    # assume methods has no parameters
    methodArgsDict = dict()
    # keep only method parameters matching local ones
    for parameter in parametersList:
        parameterName = parameter
        if hasattr(parameter, "name"):
            parameterName = parameter.name
        if parameterName in localValuesDict:
            methodArgsDict[parameterName] = localValuesDict[parameterName]
    # stringize & return method parameters
    methodArgsString = str(methodArgsDict)
    return methodArgsString
pass
