from .lang_tools import extract_vowel_form, find_main_mute_consonant
import pythainlp
from dataclasses import dataclass
from .const import *


@dataclass
class ThaiSubWord:
    def __init__(self, word: str = 'เกี๊ยว'):
        # Character base
        self._raw: str = word
        self._vowels_tup: List[str] = self.vowels_tup
        self._vowels: List[str] = self.vowels
        self._consonants_tup: List[str] = self.consonants_tup
        self._consonants: List[str] = self.consonants
        self._tone_mark: List[str] = self.tone_mark
        self._mute_mark: int = self.mute_mark
        self._two_syllable = False
        # extractions
        self.extract_vowel()

        # Type based
        self._vowel_form: str = self._ex_vw_form
        self._vowel_con_tup = self.vowel_con_tup
        self._mute_con_tup = self.mute_con_tup
        self._mute_con = self.mute_con
        self._true_con_tup = self.true_con_tup
        self._con_split = self.consonant_split_index()
        # self._init_con: str = self.init_con
        # self._final_con: str = self._ex_regex.groups()[-1]

        self._tone: str = None

    @property
    def raw(self):
        return self._raw

    @property
    def vowels_tup(self):
        return [(i, char) for i, char in enumerate(self._raw) if char in THAI_VOW]

    @property
    def vowels(self):
        return [char[1] for char in self.vowels_tup]

    @property
    def consonants_tup(self):
        return [(i, char) for i, char in enumerate(self._raw) if char in THAI_CONS]

    @property
    def consonants(self):
        return [char[1] for char in self.consonants_tup]

    @property
    def tone_mark(self):
        return [char for char in self._raw if char in THAI_TONE]

    @property
    def mute_mark(self):
        if MUTE_MARK not in self._raw:
            return -1
        else:
            return self._raw.index(MUTE_MARK)

    @property
    def vowel_con_tup(self):
        for con in reversed(self.consonants_tup):
            if con[1] in self._vowel_form:
                return con

        return (-1, None)

    @property
    def true_con_tup(self):
        true_con_tup = self.consonants_tup.copy()

        if self.vowel_con_tup[1] is not None:
            true_con_tup.remove(self.vowel_con_tup)

        for ch in self.mute_con_tup:
            true_con_tup.remove(ch)
        return true_con_tup

    @property
    def mute_con_tup(self):
        return find_main_mute_consonant(self._raw)

    @property
    def mute_con(self):
        return [ch[1] for ch in self.mute_con_tup]

    # last init con index less than or equal to
    def consonant_split_index(self):
        if len(self.tone_mark) > 0:
            return (self._raw.index(self.tone_mark[0]), self.tone_mark[0])

        elif self._vowel_form in VOWEL_FORM_BASIC:
            return self._vowels_tup[-1]

        elif self._vowel_form in VOWEL_FORMS_W_CONSONANT:  # เลีย , ทอง
            return self._vowel_con_tup

        elif self._vowel_form in VOWEL_FORMS_W_LEADING or self._vowel_form == '-':
            true_con_len = len(self.true_con_tup)
            if true_con_len == 1:  # เท , ไป, กบ
                return self.true_con_tup[0]

            elif true_con_len == 2:  # ใคร, ไหน ,เปล ,แซง
                if self.true_con_tup[0][1] + self.true_con_tup[1][1] in ALL_CONSONANT_CLUSTER:

                    return self.true_con_tup[1]
                else:
                    return self.true_con_tup[0]

            elif true_con_len == 3:
                if self.true_con_tup[0][1] + self.true_con_tup[1][1] in ALL_CONSONANT_CLUSTER:
                    return self.true_con_tup[1]
                elif self.true_con_tup[1][1] + self.true_con_tup[2][1] in DOUBLE_FINAL_CONSONANT:
                    return self.true_con_tup[0]
                else:
                    self._two_syllable = True  # ตลาด,สนม
                    print('check this case not sure')
                    return self.true_con_tup[1]
            elif true_con_len == 4:
                if self.true_con_tup[1][1] + self.true_con_tup[2][1] == 'รร':  # บรรณ
                    return self.true_con_tup[0]
                else:
                    return self.true_con_tup[1]
            else:
                return "Error Not implement"

        else:
            return "Error Not implement"

    # @property
    # def init_con(self):
    #     if len(self.true_con) == 1:
    #         return self.true_con
    #     elif len(self.true_con) > 2:
    #         return self.true_con[0:2]
    #     else:
    #         return 1

    def extract_vowel(self):
        self._ex_vw_form, self._ex_regex, self._ex_pattern = extract_vowel_form(
            self._raw)

    def __getitem__(self, key):
        return self._raw[key]

    def __setitem__(self, key, value):
        self._raw[key] = value
