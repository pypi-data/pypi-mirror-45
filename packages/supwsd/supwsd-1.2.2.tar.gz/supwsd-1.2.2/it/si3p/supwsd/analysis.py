'''
Created on 9 apr 2019

@author: papan
'''
from enum import Enum
from it.si3p.supwsd.config import License


class Pos(Enum):    
    NOUN=1,
    VERB=2,
    ADJ=3,
    ADV=4

class Result(object):
  
    def __init__(self,json):
        self._token=Token(json['token'])
        self._senses=list()
        
        for sense in json['senses']:
            self._senses.append(Sense(sense))
        
    @property
    def token(self):
        return self._token
    
    @property
    def senses(self):
        return self._senses
    
    def sense(self):
        return self.senses[0]
    
    def miss(self):
        return self.sense().id=='U'
    

class Token(object):
  
    def __init__(self,json):
        self._word=json['word']
        self._lemma=json['lemma']
        self._tag=json['tag']
        self._pos=Pos[json['pos']]
        
    @property
    def word(self):
        return self._word
    
    @property
    def lemma(self):
        return self._lemma
      
    @property
    def tag(self):
        return self._tag
    
    @property
    def pos(self):
        return self._pos
      
    def __str__(self):
        return self.word


class Sense(object):
  
    def __init__(self,json):
        self._id=json['id']
        self._probability=json['probability']
        
        if 'gloss' in json:
            self._gloss=Gloss(json['gloss'])
        else:
            self._gloss=None;
            
    @property
    def id(self):
        return self._id
    
    @property
    def probability(self):
        return self._probability
    
    @property
    def gloss(self):
        return self._gloss
    
    def __cmp__(self, other):
        return (self.probability > other.probability) - (self.probability< other.probability)
    
    def __eq__(self, other):
        return isinstance(other, Sense) and self.id == other.id
    
    def __str__(self):
        return self.id


class Gloss(object):
  
    def __init__(self,json):
        self._description=json['description']
        self._license=License[json['license']]
        
    @property
    def description(self):
        return self._description
    
    @property
    def license(self):
        return self._license
        
    def __str__(self):
        return self.description