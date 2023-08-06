# coding=utf-8
# import
from pythoncommontools.objectUtil.POPO import POPO
from datetime import datetime
# create sample classes for tests
class SampleBoolean(POPO):
    # sample function
    def sampleFunction(self):
        return self.sampleBoolean
    # contructor
    def __init__(self, sampleBoolean=False):
        self.sampleBoolean=sampleBoolean
class SampleNonStandardObject(POPO):
    # sample function
    @staticmethod
    def sampleFunction():
        return datetime.fromtimestamp(0)
    # contructor
    def __init__(self, dateTime=datetime.fromtimestamp(0)):
        self.dateTime=dateTime
class SampleNumeric(POPO):
    # sample function
    def sampleFunction(self):
        return self.sampleInt + self.sampleFloat + self.sampleComplex
    # contructor
    def __init__(self, sampleInt=0, sampleFloat=0.0, sampleComplex=complex(0, 0)):
        self.sampleInt=sampleInt
        self.sampleFloat=sampleFloat
        self.sampleComplex=sampleComplex
class SampleSequence(POPO):
    # sample function
    def sampleFunction(self):
        return len(self.sampleList) + len(self.sampleTuple) + len(self.sampleRange)
    # contructor
    def __init__(self, sampleList=list(), sampleTuple=tuple(), sampleRange=range(0, 0)):
        self.sampleList=sampleList
        self.sampleTuple=sampleTuple
        self.sampleRange=sampleRange
class SampleString(POPO):
    # sample function
    def sampleFunction(self):
        return len(self.sampleString)
    # contructor
    def __init__(self, sampleString=''):
        self.sampleString=sampleString
class SampleBinary(POPO):
    # sample function
    def sampleFunction(self):
        return len(self.sampleBytes) + len(self.sampleBytearray) + len(self.sampleMemoryview)
    # contructor
    def __init__(self, sampleBytes=bytes(), sampleBytearray=bytearray(), sampleMemoryview=memoryview(b'')):
        self.sampleBytes=sampleBytes
        self.sampleBytearray=sampleBytearray
        self.sampleMemoryview=sampleMemoryview
class SampleSet(POPO):
    # sample function
    def sampleFunction(self):
        return len(self.sampleSet) + len(self.sampleFrozenset)
    # contructor
    def __init__(self, sampleSet=set(), sampleFrozenset=frozenset()):
        self.sampleSet=sampleSet
        self.sampleFrozenset=sampleFrozenset
class SampleDictionnary(POPO):
    # sample function
    def sampleFunction(self):
        return len(self.sampleDictionnary)
    # contructor
    def __init__(self, sampleDictionnary=dict()):
        self.sampleDictionnary=sampleDictionnary
class SampleObject(POPO):
    # sample function
    def sampleFunction(self):
        return self.__dict__
    # contructor
    def __init__(self, sampleAttributs=dict()):
        for attributKey, attributValue in sampleAttributs.items():
            setattr(self, attributKey, attributValue)
        pass
    pass
# generator function
def getSampleBoolean() :
    return SampleBoolean(True)
def getSampleNonStandardObject() :
    return SampleNonStandardObject()
def getSampleNumeric() :
    return SampleNumeric(1,2.3,complex(4, 5))
def getSampleSequence() :
    # INFO : some object are not hashable, so can not be in tuple : list, dict
    innerSampleSet = set((True, 7, 4.8, complex(1, 5), b'\x1a\x2b\x3c', memoryview(b'mplokij'), None))
    innerSampleFrozenset = frozenset((True, 9, 2.6, complex(3, 0), b'\x4d\x5e\x6f', memoryview(b'wqaxszcd'), None))
    innerList = [False, 5, 6.7, complex(8, 9), b'\x0f\x1f\x2f', bytearray(b'\x3e\x4e\x5e'), memoryview(b'azerty'), None, SampleNonStandardObject(), innerSampleSet, innerSampleFrozenset]
    innerTuple = (False, 0, 8.5, complex(6, 4), b'\xa9\xb8\xc7', bytearray(b'\x6d\x5e\x4f'), memoryview(b'ascfthn'), None, SampleNonStandardObject(), innerSampleSet, innerSampleFrozenset)
    sampleSet = set((True, 3, 2.6, complex(1, 5), b'\xa1\xb2\xc3', memoryview(b'poiuytr'), None, innerSampleFrozenset))
    sampleFrozenset = frozenset((True, 9, 4.8, complex(7, 0), b'\xd4\xe5\xf6', memoryview(b'mlkjhgf'), None, innerSampleFrozenset))
    '''INFO :
     - we can not use an object as a key because a dict (i.e. the attributs) can not be a key
     - even in a frozen set'''
    innerDictionnary = {
    False: True,
    True: None,
    'a': 9,
    'b': 8.7,
    'c': complex(6, 5),
    'd': "azerty",
    'e': b'\xf0\xf1\xf2',
    'f': bytearray(b'\xe3\xe4\xe5'),
    'g': memoryview(b'abcefg'),
    'h': innerList,
    'j': None,
    0: 9,
    1: 8.7,
    2: complex(6, 5),
    3: "azerty",
    4: b'\xf0\xf1\xf2',
    5: bytearray(b'\xe3\xe4\xe5'),
    6: memoryview(b'abcefg'),
    7: innerList,
    9: None,
    10.: 9,
    9.1: 8.7,
    8.2: complex(6, 5),
    7.3: "azerty",
    6.4: b'\xf0\xf1\xf2',
    5.5: bytearray(b'\xe3\xe4\xe5'),
    4.6: memoryview(b'abcefg'),
    3.7: innerList,
    1.9: None,
    complex(1, 0): 9,
    complex(9, 1): 8.7,
    complex(8, 2): complex(6, 5),
    complex(7, 3): "azerty",
    complex(6, 4): b'\xf0\xf1\xf2',
    complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
    complex(4, 6): memoryview(b'abcefg'),
    complex(3, 7): innerList,
    complex(2, 8): None,
    b'az': 9,
    b'by': 8.7,
    b'cx': complex(6, 5),
    b'dw': "azerty",
    b'ev': b'\xf0\xf1\xf2',
    b'fu': bytearray(b'\xe3\xe4\xe5'),
    b'gt': memoryview(b'abcefg'),
    b'hs': innerList,
    b'hy': None,
    memoryview(b'er'): 1,
    memoryview(b'ty'): 2.3,
    memoryview(b'ui'): complex(4, 5),
    memoryview(b'op'): "azerty",
    memoryview(b'qs'): b'\xf0\xf1\xf2',
    memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
    memoryview(b'gh'): memoryview(b'abcefg'),
    memoryview(b'jk'): innerList,
    memoryview(b'wx'): None,
    frozenset([0, 1]): 1,
    frozenset([2.0, 3.1]): 2.3,
    frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
    frozenset(['0', '1']): "azerty",
    frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
    frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
    frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
    frozenset([2, 3]): innerList,
    frozenset([None]): None,
    "dateTime" : SampleNonStandardObject(),
    }
    sampleDictionnary = {
    True: False,
    False: None,
    'a': 1,
    'b': 2.3,
    'c': complex(4, 5),
    'd': "azerty",
    'e': b'\xf0\xf1\xf2',
    'f': bytearray(b'\xe3\xe4\xe5'),
    'g': memoryview(b'abcefg'),
    'h': innerList,
    'k': innerDictionnary,
    'l': None,
    0: 1,
    1: 2.3,
    2: complex(4, 5),
    3: "azerty",
    4: b'\xf0\xf1\xf2',
    5: bytearray(b'\xe3\xe4\xe5'),
    6: memoryview(b'abcefg'),
    7: innerList,
    10: innerDictionnary,
    11: None,
    10.: 1,
    9.1: 2.3,
    8.2: complex(4, 5),
    7.3: "azerty",
    6.4: b'\xf0\xf1\xf2',
    5.5: bytearray(b'\xe3\xe4\xe5'),
    4.6: memoryview(b'abcefg'),
    3.7: innerList,
    0.1: innerDictionnary,
    1.0: None,
    complex(1, 0): 1,
    complex(9, 1): 2.3,
    complex(8, 2): complex(4, 5),
    complex(7, 3): "azerty",
    complex(6, 4): b'\xf0\xf1\xf2',
    complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
    complex(4, 6): memoryview(b'abcefg'),
    complex(3, 7): innerList,
    complex(1, 9): innerDictionnary,
    complex(1, 0): None,
    b'az': 1,
    b'by': 2.3,
    b'cx': complex(4, 5),
    b'dw': "azerty",
    b'ev': b'\xf0\xf1\xf2',
    b'fu': bytearray(b'\xe3\xe4\xe5'),
    b'gt': memoryview(b'abcefg'),
    b'hs': innerList,
    b'ju': innerDictionnary,
    b'nb': None,
    memoryview(b'er'): 1,
    memoryview(b'ty'): 2.3,
    memoryview(b'ui'): complex(4, 5),
    memoryview(b'op'): "azerty",
    memoryview(b'qs'): b'\xf0\xf1\xf2',
    memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
    memoryview(b'gh'): memoryview(b'abcefg'),
    memoryview(b'jk'): innerList,
    memoryview(b'lm'): innerDictionnary,
    memoryview(b'wx'): None,
    frozenset([0, 1]): 1,
    frozenset([2.0, 3.1]): 2.3,
    frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
    frozenset(['0', '1']): "azerty",
    frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
    frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
    frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
    frozenset([2, 3]): innerList,
    frozenset({'jack': 4098, 12.3: complex(41, 39)}): innerDictionnary,
    frozenset([None]): None,
    "dateTime": SampleNonStandardObject(),
    }
    innerSampleObject = SampleObject({"attributSet":innerSampleSet,"attributFrozenset":innerSampleFrozenset,"attributList":innerList,"attributTuple":innerTuple,"dateTime": SampleNonStandardObject()})
    sampleList = [True, 0, 1.2, complex(3, 4), b'\xf0\xf1\xf2', bytearray(b'\xe3\xe4\xe5'), memoryview(b'abcefg'), None, SampleNonStandardObject(), sampleSet, sampleFrozenset, sampleDictionnary,innerSampleObject]
    sampleTuple = (True, 9, 8.7, complex(6, 5), b'\xa1\xb2\xc3', bytearray(b'\x4d\x5e\x6f'), memoryview(b'mlkqsdg'), None, SampleNonStandardObject(), innerTuple, sampleSet, sampleFrozenset,innerSampleObject)
    sampleRange = range(1, 10)
    return SampleSequence(sampleList, sampleTuple, sampleRange)
def getSampleString():
    sampleString = "hello world!"
    return SampleString(sampleString)
def getSampleBinary():
    sampleBytes = b'\xf0\xf1\xf2'
    sampleBytearray = bytearray(b'\xe3\xe4\xe5')
    sampleMemoryview = memoryview(b'abcefg')
    return SampleBinary(sampleBytes, sampleBytearray, sampleMemoryview)
def getSampleSet():
    # INFO : some object are not hashable, so can not be in a (frozen)set : bytearray, list, set, dict
    innerFrozenset = frozenset((True, 3, 2.6, complex(1, 9), b'\x3e\x4e\x5e', memoryview(b'wqazsxc'), None))
    sampleSet = set((True, 0, 1.2, complex(3, 4), b'\xf0\xf1\xf2', memoryview(b'abcefg'), None, innerFrozenset))
    sampleFrozenset = frozenset((True, 9, 8.7, complex(6, 5), b'\xe3\xe4\xe5', memoryview(b'azerty'), None, innerFrozenset))
    return SampleSet(sampleSet, sampleFrozenset)
def getSampleDictionnary():
    # TODO: upgrade lists & set & map
    innerSampleSet = set((True, 7, 4.8, complex(1, 5), b'\x1a\x2b\x3c', memoryview(b'mplokij'), None))
    innerSampleFrozenset = frozenset((True, 9, 2.6, complex(3, 0), b'\x4d\x5e\x6f', memoryview(b'wqaxszcd'), None))
    innerList = [False, 5, 6.7, complex(8, 9), b'\x0f\x1f\x2f', bytearray(b'\x3e\x4e\x5e'), memoryview(b'azerty'), None, SampleNonStandardObject(), innerSampleSet, innerSampleFrozenset]
    sampleSet = set((True, 3, 2.6, complex(1, 5), b'\xa1\xb2\xc3', memoryview(b'poiuytr'), None))
    sampleFrozenset = frozenset((True, 9, 4.8, complex(7, 0), b'\xd4\xe5\xf6', memoryview(b'mlkjhgf'), None))
    sampleList = [True, 0, 1.2, complex(3, 4), b'\xf0\xf1\xf2', bytearray(b'\xe3\xe4\xe5'), memoryview(b'abcefg'), None, SampleNonStandardObject(), innerList, sampleSet, sampleFrozenset]
    # INFO : some object are not hashable, so can not be in dictionnary key : bytearray, list, set, dict
    innerDictionnary = {
        False: True,
        True: None,
        'a': 9,
        'b': 8.7,
        'c': complex(6, 5),
        'd': "azerty",
        'e': b'\xf0\xf1\xf2',
        'f': bytearray(b'\xe3\xe4\xe5'),
        'g': memoryview(b'abcefg'),
        'h': innerList,
        'j': None,
        0: 9,
        1: 8.7,
        2: complex(6, 5),
        3: "azerty",
        4: b'\xf0\xf1\xf2',
        5: bytearray(b'\xe3\xe4\xe5'),
        6: memoryview(b'abcefg'),
        7: innerList,
        9: None,
        10.: 9,
        9.1: 8.7,
        8.2: complex(6, 5),
        7.3: "azerty",
        6.4: b'\xf0\xf1\xf2',
        5.5: bytearray(b'\xe3\xe4\xe5'),
        4.6: memoryview(b'abcefg'),
        3.7: innerList,
        1.9: None,
        complex(1, 0): 9,
        complex(9, 1): 8.7,
        complex(8, 2): complex(6, 5),
        complex(7, 3): "azerty",
        complex(6, 4): b'\xf0\xf1\xf2',
        complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
        complex(4, 6): memoryview(b'abcefg'),
        complex(3, 7): innerList,
        complex(2, 8): None,
        b'az': 9,
        b'by': 8.7,
        b'cx': complex(6, 5),
        b'dw': "azerty",
        b'ev': b'\xf0\xf1\xf2',
        b'fu': bytearray(b'\xe3\xe4\xe5'),
        b'gt': memoryview(b'abcefg'),
        b'hs': innerList,
        b'hy': None,
        memoryview(b'er'): 1,
        memoryview(b'ty'): 2.3,
        memoryview(b'ui'): complex(4, 5),
        memoryview(b'op'): "azerty",
        memoryview(b'qs'): b'\xf0\xf1\xf2',
        memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
        memoryview(b'gh'): memoryview(b'abcefg'),
        memoryview(b'jk'): sampleList,
        memoryview(b'wx'): None,
        frozenset([0, 1]): 1,
        frozenset([2.0, 3.1]): 2.3,
        frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
        frozenset(['0', '1']): "azerty",
        frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
        frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
        frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
        frozenset([2, 3]): sampleList,
        frozenset([None]): None,
        "dateTime": SampleNonStandardObject(),
    }
    return SampleDictionnary({
        True: False,
        False: None,
        'a': 1,
        'b': 2.3,
        'c': complex(4, 5),
        'd': "azerty",
        'e': b'\xf0\xf1\xf2',
        'f': bytearray(b'\xe3\xe4\xe5'),
        'g': memoryview(b'abcefg'),
        'h': sampleList,
        'k': innerDictionnary,
        'l': None,
        0: 1,
        1: 2.3,
        2: complex(4, 5),
        3: "azerty",
        4: b'\xf0\xf1\xf2',
        5: bytearray(b'\xe3\xe4\xe5'),
        6: memoryview(b'abcefg'),
        7: sampleList,
        10: innerDictionnary,
        11: None,
        10.: 1,
        9.1: 2.3,
        8.2: complex(4, 5),
        7.3: "azerty",
        6.4: b'\xf0\xf1\xf2',
        5.5: bytearray(b'\xe3\xe4\xe5'),
        4.6: memoryview(b'abcefg'),
        3.7: sampleList,
        0.1: innerDictionnary,
        1.0: None,
        complex(1, 0): 1,
        complex(9, 1): 2.3,
        complex(8, 2): complex(4, 5),
        complex(7, 3): "azerty",
        complex(6, 4): b'\xf0\xf1\xf2',
        complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
        complex(4, 6): memoryview(b'abcefg'),
        complex(3, 7): sampleList,
        complex(1, 9): innerDictionnary,
        complex(1, 0): None,
        b'az': 1,
        b'by': 2.3,
        b'cx': complex(4, 5),
        b'dw': "azerty",
        b'ev': b'\xf0\xf1\xf2',
        b'fu': bytearray(b'\xe3\xe4\xe5'),
        b'gt': memoryview(b'abcefg'),
        b'hs': sampleList,
        b'ju': innerDictionnary,
        b'nb': None,
        memoryview(b'er'): 1,
        memoryview(b'ty'): 2.3,
        memoryview(b'ui'): complex(4, 5),
        memoryview(b'op'): "azerty",
        memoryview(b'qs'): b'\xf0\xf1\xf2',
        memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
        memoryview(b'gh'): memoryview(b'abcefg'),
        memoryview(b'jk'): sampleList,
        memoryview(b'lm'): innerDictionnary,
        memoryview(b'wx'): None,
        frozenset([0, 1]): 1,
        frozenset([2.0, 3.1]): 2.3,
        frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
        frozenset(['0', '1']): "azerty",
        frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
        frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
        frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
        frozenset([2, 3]): sampleList,
        frozenset({'jack': 4098, 12.3: complex(41, 39)}): innerDictionnary,
        frozenset([None]): None,
        "dateTime": SampleNonStandardObject(),
    })
def getSampleObject():
    # INFO : some object are not hashable, so can not be in a (frozen)set : bytearray, list, set, dict
    # TODO: upgrade lists & set
    sampleInt = 1
    sampleFloat = 2.3
    sampleComplex = complex(4, 5)
    sampleNumeric = SampleNumeric(sampleInt, sampleFloat, sampleComplex)
    innerSampleSet = set((True, 7, 4.8, complex(1, 5), b'\x1a\x2b\x3c', memoryview(b'mplokij'), None))
    innerSampleFrozenset = frozenset((True, 9, 2.6, complex(3, 0), b'\x4d\x5e\x6f', memoryview(b'wqaxszcd'), None))
    innerList = [False, 5, 6.7, complex(8, 9), b'\x0f\x1f\x2f', bytearray(b'\x3e\x4e\x5e'), memoryview(b'azerty'), None, SampleNonStandardObject(), innerSampleSet, innerSampleFrozenset]
    sampleSet = set((True, 3, 2.6, complex(1, 5), b'\xa1\xb2\xc3', memoryview(b'poiuytr'), None, innerSampleFrozenset))
    sampleFrozenset = frozenset((True, 9, 4.8, complex(7, 0), b'\xd4\xe5\xf6', memoryview(b'mlkjhgf'), None, innerSampleFrozenset))
    innerDictionnary = {
        False: True,
        True: None,
        'a': 9,
        'b': 8.7,
        'c': complex(6, 5),
        'd': "azerty",
        'e': b'\xf0\xf1\xf2',
        'f': bytearray(b'\xe3\xe4\xe5'),
        'g': memoryview(b'abcefg'),
        'h': innerList,
        'j': None,
        0: 9,
        1: 8.7,
        2: complex(6, 5),
        3: "azerty",
        4: b'\xf0\xf1\xf2',
        5: bytearray(b'\xe3\xe4\xe5'),
        6: memoryview(b'abcefg'),
        7: innerList,
        9: None,
        10.: 9,
        9.1: 8.7,
        8.2: complex(6, 5),
        7.3: "azerty",
        6.4: b'\xf0\xf1\xf2',
        5.5: bytearray(b'\xe3\xe4\xe5'),
        4.6: memoryview(b'abcefg'),
        3.7: innerList,
        1.9: None,
        complex(1, 0): 9,
        complex(9, 1): 8.7,
        complex(8, 2): complex(6, 5),
        complex(7, 3): "azerty",
        complex(6, 4): b'\xf0\xf1\xf2',
        complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
        complex(4, 6): memoryview(b'abcefg'),
        complex(3, 7): innerList,
        complex(2, 8): None,
        b'az': 9,
        b'by': 8.7,
        b'cx': complex(6, 5),
        b'dw': "azerty",
        b'ev': b'\xf0\xf1\xf2',
        b'fu': bytearray(b'\xe3\xe4\xe5'),
        b'gt': memoryview(b'abcefg'),
        b'hs': innerList,
        b'hy': None,
        memoryview(b'er'): 1,
        memoryview(b'ty'): 2.3,
        memoryview(b'ui'): complex(4, 5),
        memoryview(b'op'): "azerty",
        memoryview(b'qs'): b'\xf0\xf1\xf2',
        memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
        memoryview(b'gh'): memoryview(b'abcefg'),
        memoryview(b'jk'): innerList,
        memoryview(b'wx'): None,
        frozenset([0, 1]): 1,
        frozenset([2.0, 3.1]): 2.3,
        frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
        frozenset(['0', '1']): "azerty",
        frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
        frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
        frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
        frozenset([2, 3]): innerList,
        frozenset([None]): None,
        "dateTime": SampleNonStandardObject(),
    }
    sampleDictionnary = {
        True: False,
        False: None,
        'a': 1,
        'b': 2.3,
        'c': complex(4, 5),
        'd': "azerty",
        'e': b'\xf0\xf1\xf2',
        'f': bytearray(b'\xe3\xe4\xe5'),
        'g': memoryview(b'abcefg'),
        'h': innerList,
        'k': innerDictionnary,
        'l': None,
        0: 1,
        1: 2.3,
        2: complex(4, 5),
        3: "azerty",
        4: b'\xf0\xf1\xf2',
        5: bytearray(b'\xe3\xe4\xe5'),
        6: memoryview(b'abcefg'),
        7: innerList,
        10: innerDictionnary,
        11: None,
        10.: 1,
        9.1: 2.3,
        8.2: complex(4, 5),
        7.3: "azerty",
        6.4: b'\xf0\xf1\xf2',
        5.5: bytearray(b'\xe3\xe4\xe5'),
        4.6: memoryview(b'abcefg'),
        3.7: innerList,
        0.1: innerDictionnary,
        1.0: None,
        complex(1, 0): 1,
        complex(9, 1): 2.3,
        complex(8, 2): complex(4, 5),
        complex(7, 3): "azerty",
        complex(6, 4): b'\xf0\xf1\xf2',
        complex(5, 5): bytearray(b'\xe3\xe4\xe5'),
        complex(4, 6): memoryview(b'abcefg'),
        complex(3, 7): innerList,
        complex(1, 9): innerDictionnary,
        complex(1, 0): None,
        b'az': 1,
        b'by': 2.3,
        b'cx': complex(4, 5),
        b'dw': "azerty",
        b'ev': b'\xf0\xf1\xf2',
        b'fu': bytearray(b'\xe3\xe4\xe5'),
        b'gt': memoryview(b'abcefg'),
        b'hs': innerList,
        b'ju': innerDictionnary,
        b'nb': None,
        memoryview(b'er'): 1,
        memoryview(b'ty'): 2.3,
        memoryview(b'ui'): complex(4, 5),
        memoryview(b'op'): "azerty",
        memoryview(b'qs'): b'\xf0\xf1\xf2',
        memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
        memoryview(b'gh'): memoryview(b'abcefg'),
        memoryview(b'jk'): innerList,
        memoryview(b'lm'): innerDictionnary,
        memoryview(b'wx'): None,
        frozenset([0, 1]): 1,
        frozenset([2.0, 3.1]): 2.3,
        frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
        frozenset(['0', '1']): "azerty",
        frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
        frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
        frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
        frozenset([2, 3]): innerList,
        frozenset({'jack': 4098, 12.3: complex(41, 39)}): innerDictionnary,
        frozenset([None]): None,
        "dateTime": SampleNonStandardObject(),
    }
    sampleList = [True, 0, 1.2, complex(3, 4), b'\xf0\xf1\xf2', bytearray(b'\xe3\xe4\xe5'), memoryview(b'abcefg'), None, SampleNonStandardObject(),
                  innerList, sampleSet, sampleFrozenset, sampleDictionnary]
    sampleTuple = (3, 4.5)
    sampleRange = range(1, 10)
    sampleSequence = SampleSequence(sampleList, sampleTuple, sampleRange)
    sampleString = "hello world!"
    sampleBytes = b'\xf0\xf1\xf2'
    sampleBytearray = bytearray(b'\xe3\xe4\xe5')
    sampleMemoryview = memoryview(b'abcefg')
    sampleBinary = SampleBinary(sampleBytes, sampleBytearray, sampleMemoryview)
    sampleSet = SampleSet(sampleSet, sampleFrozenset)
    sampleDictionnary = SampleDictionnary(sampleDictionnary)
    sampleAttributs = {
        "sampleBoolean": True,
        "sampleNumeric": sampleNumeric,
        "sampleSequence": sampleSequence,
        "sampleString": sampleString,
        "sampleBinary": sampleBinary,
        "sampleSet": sampleSet,
        "sampleDictionnary": sampleDictionnary,
    }
    return SampleObject(sampleAttributs)
    pass
# instance objects for tests
testSampleBoolean = getSampleBoolean()
testSampleNonStandardObject = getSampleNonStandardObject()
testSampleNumeric = getSampleNumeric()
testSampleSequence = getSampleSequence()
testSampleString = getSampleString()
testSampleBinary = getSampleBinary()
testSampleSet = getSampleSet()
testSampleDictionnary = getSampleDictionnary()
testSampleObject = getSampleObject()
pass
