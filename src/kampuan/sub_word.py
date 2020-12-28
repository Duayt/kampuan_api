from .lang_tools import extract_vowel_form, find_main_mute_consonant, find_mute_vowel, determine_tone_sound
import pythainlp
from dataclasses import dataclass
from .const import *


class ThaiSubWord:
    def __init__(self, word: str = 'เกี๊ยว'):
        # Character base
        if len(word) == 1 and word in THAI_CONS:
            word = word + 'ะ'
        self._raw: str = word
        self._vowels_tup: List[str] = self.vowels_tup
        self._vowels: List[str] = self.vowels
        self._consonants_tup: List[str] = self.consonants_tup
        self._consonants: List[str] = self.consonants
        self._tone_mark: List[str] = self.tone_mark
        self._mute_mark: int = self.mute_mark

        # extractions
        self.extract_vowel()

        # mute stuff
        self._mute_con_tup = self.mute_con_tup
        self._mute_con = self.mute_con
        self._mute_vow_tup = self.mute_vow_tup

        # Vowel based
        self._vowel_form: str = self._ex_vw_form
        self._vowel_con_tup = self.vowel_con_tup
        self._vowel_form_tup = self.vowel_form_tup
        self._vowel_form_tup.sort()

        # Consonant stuff
        self._true_con_tup = self.true_con_tup
        self._double_r = len(self._true_con_tup) > 2 and (
            self.true_con_tup[1][1] + self.true_con_tup[2][1] == 'รร')
        self._con_split = self.consonant_split_index()
        self.split_con()
        self.init_con = ''.join(tup[1] for tup in self._init_con_tup)
        self.final_con = ''.join(tup[1] for tup in self._final_con_tup)
        self._two_syllable = self.two_syllable

        # word types
        self._vowel_form_sound = self.vowel_form_sound
        self._vowel_class = 'short' if self._vowel_form_sound in SHORT_SOUND_VOWELS else 'long'
        self._word_class = self.word_class

        #Tone and sound
        if self.two_syllable:
            pass
        else:
            self._main_init_sound = self.main_init_sound
            self._init_sound_class = SOUND_CLASS[self._main_init_sound]
            self._aspirate = self._main_init_sound in ASPIRATE
            self._tone_mark_class = 0 if len(
                self._tone_mark) == 0 else TONE_MARK_CLASS[self._tone_mark[0]]
            self._tone_group_rule = self.tone_group_rule
            try:
                self._tone = determine_tone_sound(tone_mark_class=self._tone_mark_class,
                                                  tone_group_rule=self._tone_group_rule,
                                                  word_class=self._word_class,
                                                  vowel_class=self._vowel_class)
            except:
                print(self._raw, 'tone error')

    @property
    def vowel_form_sound(self):
        if self._double_r:
            return '-ั'
        else:
            return self._vowel_form

    @property
    def tone_group_rule(self):
        if self._init_sound_class == 'mid':
            return 0
        elif self._init_sound_class == 'high' or (self.init_con in LEADING_CONSONANT_CLUSTER):
            return 1
        elif self._init_sound_class == 'low':
            return 2

    @property
    def main_init_sound(self):
        if len(self.init_con) < 2:
            return self._init_con_tup[0][1]
        else:
            if 'ทร' == self.init_con:
                if 'ทรั' in self._raw or 'ทร็' in self._raw:  # ทรัส
                    return self._init_con_tup[0][1]
                else:
                    return 'ซ'
            elif self.init_con in TRUE_CONSONANT_CLUSTER + FALSE_CONSONANT_CLUSTER:
                return self._init_con_tup[0][1]
            elif self.init_con in LEADING_CONSONANT_CLUSTER:
                return self._init_con_tup[1][1]
            else:
                assert self._two_syllable == True
                # raise ValueError('not implement')

    @property
    def word_class(self):
        if len(self.final_con) == 0:
            if self._vowel_form_sound in LONG_SOUND_VOWELS + SHORT_LIVE_VOWELS:
                return 'live'
            else:
                return 'dead'
        else:
            if self.final_con in SORONANT:
                return 'live'
            else:
                return 'dead'

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
    def vowel_form_tup(self):
        vowel_tup = self.vowels_tup.copy()
        if len(self._mute_vow_tup) > 0:
            vowel_tup.remove(self._mute_vow_tup[0])
        if self.vowel_con_tup[0] == -1:
            return vowel_tup
        else:
            vowel_form_tup = vowel_tup + [self._vowel_con_tup]
            vowel_form_tup.sort()
            return vowel_form_tup

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
    def mute_vow_tup(self):
        return find_mute_vowel(self._raw)

    @property
    def mute_con(self):
        return [ch[1] for ch in self.mute_con_tup]

    # last init con index less than or equal to
    def consonant_split_index(self):
        if len(self.tone_mark) > 0:
            return (self._raw.index(self.tone_mark[0]), self.tone_mark[0])
        elif self._vowel_form in VOWEL_FORM_BASIC:
            return self._vowel_form_tup[-1]

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
                # โทรม, เพลง
                if self.true_con_tup[0][1] + self.true_con_tup[1][1] in ALL_CONSONANT_CLUSTER:
                    return self.true_con_tup[1]
                elif self.true_con_tup[1][1] + self.true_con_tup[2][1] in DOUBLE_FINAL_CONSONANT:
                    return self.true_con_tup[0]
                else:
                    # self._two_syllable = True  # ตลาด,สนม ,เกษม
                    print('check this case not sure')
                    return self.true_con_tup[1]
            elif true_con_len == 4:
                if self._double_r:  # บรรณ
                    return self.true_con_tup[0]
                else:
                    return self.true_con_tup[1]
            else:
                return "Error Not implement"

        else:
            return "Error Not implement"

    @property
    def two_syllable(self):
        if len(self._init_con_tup) >= 2 and (self._init_con_tup[0][1] + self._init_con_tup[1][1] not in ALL_CONSONANT_CLUSTER):
            return True
        else:
            return False

    def split_con(self):
        self._init_con_tup = []
        self._final_con_tup = []

        for tup in self.true_con_tup:
            if tup[0] <= self._con_split[0] and tup[0] != self._vowel_con_tup:
                self._init_con_tup.append(tup)
            else:
                break

        self._final_con_tup = [
            tup for tup in self.true_con_tup if tup not in self._init_con_tup]
        if self._double_r:
            self._final_con_tup = [self._final_con_tup[-1]]

    def get_tup(self):
        return [(i, j) for i, j in enumerate(self._raw)]

    def extract_vowel(self):
        self._ex_vw_form, self._ex_regex, self._ex_pattern = extract_vowel_form(
            self._raw)

    def __getitem__(self, key):
        return self._raw[key]

    def __setitem__(self, key, value):
        self._raw[key] = value

    def __str__(self):
        return self._raw

    def __repr__(self):
        return f"<{type(self).__qualname__ +' ' +str(self)} at {hex(id(self))}>"

    def split_non_conform(self):
        if self.two_syllable:
            first_init, second_init = self._init_con_tup
            first = ThaiSubWord(word=str(first_init[1])+'ะ')
            new_word = self.raw
            index = first_init[0]
            if second_init[1] in SORONANT:
                new_word = new_word[:index] + 'ห' + \
                    new_word[index + 1:]  # สวัส =>  สะ หวัด
            else:
                new_word = new_word[:index] + '' + \
                    new_word[index + 1:]  # ผดุง =>  ผะ ดุง
            second = ThaiSubWord(word=new_word)
            return [first, second]
        else:
            return [self]
