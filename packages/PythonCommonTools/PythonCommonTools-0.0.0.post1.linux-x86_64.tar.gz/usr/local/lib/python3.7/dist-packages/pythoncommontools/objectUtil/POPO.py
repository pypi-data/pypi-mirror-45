# coding=utf-8
# import
from copy import copy
from pythoncommontools.objectUtil.objectUtil import dumpObjetToDict, loadObjectFromDict, objectStringRepresentation, objectHash, objectComparison
from pythoncommontools.jsonEncoderDecoder.simpleJsonEncoderDecoder import dumpObjectToSimpleJson, loadObjectFromSimpleJson
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import dumpObjectToComplexJson, loadObjectFromComplexJson
# normalize POPO attribut
# INFO : this method is not in objectUtil file to avoid circular dependencies
def normalizePopoAttribut(popoAttribut):
    popoAttributType = type(popoAttribut)
    if issubclass(popoAttributType, POPO):
        normalizedPopo = popoAttribut.instanciateNormalize()
    elif popoAttributType in {list, tuple}:
        normalizedPopo = [normalizePopoAttribut(_) for _ in popoAttribut]
    elif popoAttributType in {set, frozenset}:
        normalizedPopo = normalizePopoAttribut(list(popoAttribut))
        normalizedPopo = frozenset(normalizedPopo)
    elif popoAttributType == dict:
        normalizedPopo = {}
        for key, value in popoAttribut.items():
            normalizedPopo[key] = normalizePopoAttribut(value)
        pass
    elif hasattr(popoAttribut,"__dict__"):
        normalizedPopo = copy(popoAttribut)
        for attribute, value in popoAttribut.__dict__.items():
            newValue = normalizePopoAttribut(value)
            setattr(normalizedPopo, attribute, newValue)
        pass
    else:
        normalizedPopo = popoAttribut
    return normalizedPopo
# global initialization
''' POPO (Plain Old Python Object)
INFO : it is not the French word for poop, but an equivalent of Java POJO & Bean'''
class POPO :
    # dictionary
    # INFO : we can not overload __dict__ property because it raise a infinite recursive loop
    def dumpToDict(self):
        return dumpObjetToDict(self)
    # representations
    def __repr__(self):
        return objectStringRepresentation(self)
    def __str__(self):
        return self.__repr__()
    # comparisons
    def __hash__(self):
        return objectHash(self)
    def __eq__(self, other):
        normalizedSelf = self.instanciateNormalize()
        if hasattr(other,"instanciateNormalize"):
            normalizedOther = other.instanciateNormalize()
        else:
            normalizedOther = other
        return objectComparison(normalizedSelf, normalizedOther)
    # contructor
    # instanciate a POPO from a dictionary
    @staticmethod
    def loadFromDict(baseDict):
        instantiatedObject = loadObjectFromDict(baseDict)
        return instantiatedObject
    '''INFO :
     - sometime, external libraries define custom primitive objects (i.e. ndarrays from numpy)
       those objects are hard to manipulate (compare or dump into JSON)
       so, they need to be normalized for such purpose
     - this method is just a stub, overide if needed in your context
    '''
    def instanciateNormalize(self):
        # INFO : do not use dumpToDict to keep inner object as is
        normalizedSelf = copy(self)
        for attribute, value in self.__dict__.items():
            newValue = normalizePopoAttribut(value)
            setattr(normalizedSelf, attribute, newValue)
        return normalizedSelf
    '''INFO :
     - following methods is not in Java POJO & Bean, but they are usefull
     - simple methods simply convert non JSON data types to string
     - complexes methods convert non JSON data types to JSON compatible surrogate types
    '''
    # dump simple JSON
    def dumpToSimpleJson(self):
        dumpedJson = dumpObjectToSimpleJson(self)
        return dumpedJson
    # load simple JSON
    @staticmethod
    def loadFromSimpleJson(json):
        instantiatedObject = loadObjectFromSimpleJson(json)
        return instantiatedObject
    # dump complex JSON
    def dumpToComplexJson(self):
        dumpedJson = dumpObjectToComplexJson(self)
        return dumpedJson
    # load complex JSON
    @staticmethod
    def loadFromComplexJson(json):
        instantiatedObject = loadObjectFromComplexJson(json)
        return instantiatedObject
    pass
pass
