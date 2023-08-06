# coding=utf-8
# @see : https://pymotw.com/2/json/ (it is for python 2, but it is adaptable for python 3)
# imports
from pythoncommontools.objectUtil.objectUtil import EncryptionMarkup, loadObjectFromDict
from copy import copy
from pythoncommontools.jsonEncoderDecoder.simpleJsonEncoderDecoder import dumpObjectToSimpleJson, loadObjectFromSimpleJson
# serializable surrogate types
class ComplexeSurrogate:
    def __init__(self,originalObject=complex(0,0)):
        self.real=originalObject.real
        self.imaginary=originalObject.imag
        pass
    pass
class RangeSurrogate:
    def __init__(self,originalObject=range(0,0)):
        self.start=originalObject.start
        self.stop=originalObject.stop
        self.step=originalObject.step
        pass
    pass
class BytesSurrogate:
    def __init__(self,originalObject=bytes()):
        self.list=list(originalObject)
        pass
    pass
class BytearraySurrogate:
    def __init__(self,originalObject=bytearray()):
        self.list=list(originalObject)
        pass
    pass
class MemoryviewSurrogate:
    def __init__(self,originalObject=memoryview(b'')):
        self.list=list(originalObject)
        pass
    pass
class TupleSurrogate:
    def __init__(self,originalObject=tuple()):
        self.list=[convertObjectToComplexJsonObject(_) for _ in originalObject]
        pass
    pass
class SetSurrogate:
    def __init__(self,originalObject=set()):
        self.list=[convertObjectToComplexJsonObject(_) for _ in originalObject]
        pass
    pass
class FrozensetSurrogate:
    def __init__(self,originalObject=frozenset()):
        self.list=[convertObjectToComplexJsonObject(_) for _ in originalObject]
        pass
    pass
# concert a dictionnary key to a JSON name
# INFO : in a JSON, names can only be string
def convertDictKeyToJsonName(keyValue,keyType):
    if keyType in {list, tuple, set, frozenset}:
        keyString = [IterableKeyElementSurrogate(_) for _ in keyValue]
    elif keyType == range:
        keyString = [keyType.start ,keyType.stop ,keyType.step]
    elif keyType in {bytes,bytearray}:
        keyString = keyValue.decode()
    elif keyType == memoryview:
        keyString = bytes(keyValue).decode()
    else :
        # INFO : shallow copy to avoid modifying original object
        keyString = copy(keyValue)
    return keyString
# INFO : can not be dynamicaly loaded if embedded in 'dict surrogate'
class IterableKeyElementSurrogate:
    def __init__(self, originalObject=None):
        elementType = type(originalObject)
        self.keyType = elementType.__name__
        self.keyValue = convertDictKeyToJsonName(originalObject, elementType)
        pass
    pass
class ItemSurrogate:
    def __init__(self, originalItem=((None,None))):
        key = originalItem[0]
        keyType = type(key)
        self.keyType = keyType.__name__
        self.keyValue = convertDictKeyToJsonName(key, keyType)
        self.value = convertObjectToComplexJsonObject(originalItem[1])
        pass
    pass
class DictSurrogate:
    def __init__(self,originalDict=dict()):
        # initiate data list
        self.list=list()
        # populate data list
        for item in originalDict.items():
            currentItemSurrogate = ItemSurrogate(item)
            self.list.append(currentItemSurrogate)
        pass
    pass
pass
# complex JSON conversion
def convertObjectToComplexJsonObject(objectToConvert):
    '''
    convert to JSON complex object
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    '''
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        # INFO : shallow copy to avoid modifying original object
        complexJSonObject = copy(objectToConvert)
        # continue convertion deeper
        shallowAttributs = objectToConvert.__dict__
        for attribut, oldValue in shallowAttributs.items():
            newValue = convertObjectToComplexJsonObject(oldValue)
            setattr(complexJSonObject, attribut, newValue)
        pass
    elif type(objectToConvert) == complex:
        complexJSonObject = ComplexeSurrogate(objectToConvert)
    elif type(objectToConvert) == range:
        complexJSonObject = RangeSurrogate(objectToConvert)
    elif type(objectToConvert) == bytes:
        complexJSonObject = BytesSurrogate(objectToConvert)
    elif type(objectToConvert) == bytearray:
        complexJSonObject = BytearraySurrogate(objectToConvert)
    elif type(objectToConvert) == memoryview:
        complexJSonObject = MemoryviewSurrogate(objectToConvert)
    elif type(objectToConvert) == list:
        complexJSonObject = [convertObjectToComplexJsonObject(_) for _ in objectToConvert]
    elif type(objectToConvert) == tuple:
        complexJSonObject = TupleSurrogate(objectToConvert)
    elif type(objectToConvert) == set:
        complexJSonObject = SetSurrogate(objectToConvert)
    elif type(objectToConvert) == frozenset:
        complexJSonObject = FrozensetSurrogate(objectToConvert)
    elif type(objectToConvert) == dict:
        complexJSonObject = DictSurrogate(objectToConvert)
    else :
        # INFO : shallow copy to avoid modifying original object
        complexJSonObject = copy(objectToConvert)
    # return dict
    return complexJSonObject
def dumpObjectToComplexJson(objectToDump):
    # copy & adapt data to dump
    complexJSonObject = convertObjectToComplexJsonObject(objectToDump)
    # dump & return
    dumpedJson = dumpObjectToSimpleJson(complexJSonObject)
    return dumpedJson
# regenerete exact key list
def regenerateKeysList(keys):
    fullLoadedKeySurrogates = [loadObjectFromDict(_) for _ in keys]
    regeneratedKeys = [regenerateKey(_.keyType, _.keyValue) for _ in fullLoadedKeySurrogates]
    return regeneratedKeys
# regenerete exact key
def regenerateKey(keyType,keyValue):
    if keyType == "NoneType":
        regeneratedKey = None
    elif keyType == "complex":
        regeneratedKey = complex(keyValue)
    elif keyType == "bytes":
        regeneratedKey = keyValue.encode()
    elif keyType == "bytearray":
        regeneratedKey = bytearray(keyValue.encode())
    elif keyType == "memoryview":
        regeneratedKey = memoryview(keyValue.encode())
    elif keyType == "range":
        regeneratedKey = range(keyValue[0],keyValue[1],keyValue[2])
    elif keyType == "list":
        regeneratedKey = regenerateKeysList(keyValue)
    elif keyType == "tuple":
        regeneratedKeys = regenerateKeysList(keyValue)
        regeneratedKey = tuple(regeneratedKeys)
    elif keyType == "set":
        regeneratedKeys = regenerateKeysList(keyValue)
        regeneratedKey = set(regeneratedKeys)
    elif keyType == "frozenset":
        regeneratedKeys = regenerateKeysList(keyValue)
        regeneratedKey = frozenset(regeneratedKeys)
    else:
        # INFO : shallow copy to avoid modifying original object
        regeneratedKey = copy(keyValue)
        pass
    return regeneratedKey
def convertComplexJsonObjectToObject(objectToConvert):
    '''
    convert to JSON complex object
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    '''
    if type(objectToConvert) == ComplexeSurrogate:
        finalObject = complex(objectToConvert.real,objectToConvert.imaginary)
    elif type(objectToConvert) == RangeSurrogate:
            finalObject = range(objectToConvert.start, objectToConvert.stop, objectToConvert.step)
    elif type(objectToConvert) == BytesSurrogate:
        finalObject = bytes(objectToConvert.list)
    elif type(objectToConvert) == BytearraySurrogate:
        finalObject = bytearray(objectToConvert.list)
    elif type(objectToConvert) == MemoryviewSurrogate:
        finalObject = memoryview(bytes(objectToConvert.list))
    elif type(objectToConvert) == list:
        finalObject = [convertComplexJsonObjectToObject(_) for _ in objectToConvert]
    elif type(objectToConvert) == TupleSurrogate:
        surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
        finalObject = tuple(surrogateList)
    elif type(objectToConvert) == SetSurrogate:
        surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
        finalObject = set(surrogateList)
    elif type(objectToConvert) == FrozensetSurrogate:
        surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
        finalObject = frozenset(surrogateList)
    elif type(objectToConvert) == DictSurrogate:
        # load all item surrogate
        fullLoadedItemSurrogates = [loadObjectFromDict(_) for _ in objectToConvert.list]
        # generate final dictionary
        finalObject = {}
        for itemSurrogate in fullLoadedItemSurrogates:
            regeneratedKey = regenerateKey(itemSurrogate.keyType, itemSurrogate.keyValue)
            value = convertComplexJsonObjectToObject(itemSurrogate.value)
            finalObject[regeneratedKey] = value
            pass
    elif type(objectToConvert) == dict:
        # load dumped to dictionary object
        if EncryptionMarkup.CLASS_NAME.value in objectToConvert and EncryptionMarkup.MODULE.value in objectToConvert:
            rawObject = loadObjectFromDict(objectToConvert)
            finalObject = convertComplexJsonObjectToObject(rawObject)
        # load a standard dictionary
        else :
            finalObject = {}
            for key, oldValue in objectToConvert.items():
                newValue = convertComplexJsonObjectToObject(oldValue)
                finalObject[key] = newValue
            pass
    elif hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        # INFO : shallow copy to avoid modifying original object
        finalObject = copy(objectToConvert)
        shallowAttributs = objectToConvert.__dict__
        for attribut, oldValue in shallowAttributs.items():
            newValue = convertComplexJsonObjectToObject(oldValue)
            setattr(finalObject, attribut, newValue)
    else:
        # INFO : shallow copy to avoid modifying original object
        finalObject = copy(objectToConvert)
        pass
    # return dict
    return finalObject
def loadObjectFromComplexJson(json):
    instantiatedObject = loadObjectFromSimpleJson(json)
    finalObject = convertComplexJsonObjectToObject(instantiatedObject)
    return finalObject
pass