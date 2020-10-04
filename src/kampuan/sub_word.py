import pythainlp
from dataclasses import dataclass


@dataclass
class ThaiSubWord:
    def __init__(self, word:str='เกี๊ยว'):
        # Character base
        self._raw: str=word
        self._vowels:List[str]=self.vowels
        self._consonants:List[str]=self.consonants
        self._tone_mark:List[str]=self.tone_mark
        
        # Type based
        self._inti_con:str =None
        self._final_con:str=None
        self._vowel_form:str=None
        self._tone:str=None
    
    @property
    def raw(self):
        return self._raw
    
    @property
    def vowels(self):
        return [char for char in self._raw if char in THAI_VOW]
    
    @property
    def consonants(self):
        return [char for char in self._raw if char in THAI_CONS]
    
    @property
    def tone_mark(self):
        return [char for char in self._raw if char in THAI_TONE]
    