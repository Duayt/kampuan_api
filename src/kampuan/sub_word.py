import pythainlp
from dataclasses import dataclass
from .const import THAI_VOW, THAI_TONE, THAI_CONS
from .lang_tools import extract_vowel_form


@dataclass
class ThaiSubWord:
    def __init__(self, word: str = 'เกี๊ยว'):
        # Character base
        self._raw: str = word
        self._vowels: List[str] = self.vowels
        self._consonants: List[str] = self.consonants
        self._tone_mark: List[str] = self.tone_mark

        # extractions
        self.extract_vowel()

        # Type based
        self._vowel_form: str = self._ex_vw_form
        self._vowel_con = self.vowel_con
        self._true_con = self.true_con
        self._init_con: str =self.init_con
        self._final_con: str = self._ex_regex.groups()[-1]

        self._tone: str = None

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

    @property
    def vowel_con(self):
        return [ch for ch in self._vowel_form if ch in self.consonants]

    @property
    def true_con(self):
        true_con = self.consonants.copy()
        for ch in self.vowel_con:
            true_con.remove(ch)
        return true_con

    @property
    def init_con(self):
        if len(self.true_con) == 1:
            return self.true_con
        elif len(self.true_con) > 2:
            return self.true_con[0:2]
        else:
            return 1

    def extract_vowel(self):
        self._ex_vw_form, self._ex_regex, self._ex_pattern = extract_vowel_form(
            self._raw)

    def __getitem__(self, key):
        return self._raw[key]

    def __setitem__(self, key, value):
        self._raw[key] = value
