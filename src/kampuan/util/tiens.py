import re
from kampuan.util import LCSubStr


class thai_subwords():
    """Design to take input as single Thai token or word and extract start, vowel, end and sound of said token
    For additional data regarding different Thai words types and pronunciations, 
    consult:https://sites.google.com/site/phasathaionline/hnwy-kar-reiyn-ru2/phyaychnatn"""

    def __init__(self, orig_word, debug=False):
        self.orig_word = orig_word  # Try not to change this value
        self._start = ''
        self._vowel = ''
        self._end = ''
        self._sound = ''
        # used to flag with that has two starting alphabets with sound like 'ตลาด = ตะ ลาด'
        self._double_start_sound = False
        self._high_lead_low = False  # case อักษรสูงนำอักษรต่ำ
        self.debug = debug

        # Need to deal with negative lookahead case for word like "เกรียน" to correctly extract กร
        self.vowels_form = ['ะ', ' ั' ' ็', 'า', ' ิ', ' ่', " ่", ' ํ',
                            ' ุ', ' ู', 'เ', 'ใ', 'ไ', 'โ', 'อ', 'ย', 'ว', 'ฤ', 'ฤๅ', 'ฦ', 'ฦๅ']
        combine_vowel_regex_1 = '(?!เ.{1,4}ี.*ย)(?!เ.{1,4}ี.*ยะ)(?!เ.{1,4}ื.*อ)(?!เ.{1,4}ื.*อะ)(?!เ.{1,4}.*อะ)(?!เ.{1,4}.*อ)(?!เ.{1,4}.*าะ)'
        combine_vowel_regex_2 = '(?!เ.{1,4}.*า)(?!แ.{1,4}.*า)(?!.{1,4}ัวะ)(?!โ.{1,4}.*ะ)'
        combine_vowel_regex = combine_vowel_regex_1 + combine_vowel_regex_2
        self.start_regex_1 = ['(.{1,4})ะ', '(.{1,4})า', '(.{1,4})ิ.*', '(.{1,4})ี.*', '(.{1,4})ึ', '(.{1,4})ื.*', '(.{1,4})ุ.*', '(.{1,4})ู.*', 'เ(.{1,4})็',
                              'เ(.{1,4}).*', '(.{1,4}).*อ', 'แ(.{1,4}).*', '(.{1,4})ั.*', 'โ(.{1,4}).*', '(.{1,4}).*ำ', 'ใ(.{1,4}).*', 'ไ(.{1,4})']
        self.start_regex_1 = [combine_vowel_regex +
                              regex for regex in self.start_regex_1]
        self.start_regex_2 = ['เ(.{1,4})ี.*ยะ', 'เ(.{1,4})ี.*ย', 'เ(.{1,4})ื.*อะ', 'เ(.{1,4})ื.*อ', 'เ(.{1,4}).*อ', 'เ(.{1,4}).*อะ',
                              'เ(.{1,4}).*า',
                              'เ(.{1,4}).*าะ', 'แ(.{1,4}).*ะ', '(.{1,4})ัวะ', 'โ(.{1,4}).*ะ', 'เ(.{1,4})็', 'เ(.{1,4})ิ.*']
        self.end_regex_1 = ['\[REP\]า(.{1,4})', '\[REP\]ิ(.{1,4})', '\[REP\]ี(.{1,4})', '\[REP\]ึ(.{1,4})', '\[REP\]ือ(.{1,4})',
                            '\[REP\]ุ(.{1,4})', '\[REP\]ู(.{1,4})', 'เ\[REP\]็(.{1,4})', 'เ\[REP\](.{1,4})', '\[REP\]อ(.{1,4})',
                            'แ\[REP\](.{1,4})', '\[REP\]ั(.{1,4})', 'โ\[REP\](.{1,4})', '\[REP\]ำ(.{1,4})', 'ใ\[REP\](.{1,4})',
                            'ไ\[REP\](.{1,4})']
        self.end_regex_2 = ['เ\[REP\]ีย(.{1,4})', 'เ\[REP\]ือ(.{1,4})',
                            'เ\[REP\]อ(.{1,4})', 'เ\[REP\]อะ(.{1,4})', 'เ\[REP\]า(.{1,4})']

        self.start_regex = self.start_regex_1 + self.start_regex_2
        self.end_regex = self.end_regex_1 + self.end_regex_2
        #self.vowel_regex = vowel_regex
        #self.end_regex = end_regex
        self.sound_regex = ['(่)', '(้)', '.(๊)', '()๋']

        # initialize the special character cases
        # คำควบแท้
        self.two_char_combine = ['กร', 'กล', 'กว', 'คร', 'ขร', 'คล', 'ขล', 'คว', 'ขว', 'ตร', 'ปร', 'ปล', 'พร', 'พล', 'ผล',
                                 'บร', 'บล', 'ดร', 'ฟร', 'ฟล', 'ทร', 'จร', 'ซร', 'ปร', 'สร']
        # คำนำ
        self.lead_char_nosound = ['อย', 'หง', 'หญ',
                                  'หน', 'หม', 'หย', 'หร', 'หล', 'หว']
        # อักษรสูงนำอักษรต่ำ
        self._lead_char_high_low = [
            'ขน', 'ขม', 'สม', 'สย', 'สน', 'ขย', 'ฝร', 'ถล', 'ผว', 'ตน', 'จม', 'ตล', ]
        # อักษรสูงนำอักษรกลาง
        self._high_char_high_medium = ['ผท', 'ผด', 'ผก', 'ผอ', 'ผช']

    # using property decorator

    @property
    def start(self):
        #print("getter method called")
        temp_start = self.match_pattern(self.orig_word, self.start_regex)
        if len(temp_start) == 1:
            return temp_start
        else:
            return self.check_double_start_alphabets(temp_start)
        # return self.match_pattern(self.orig_word, self.start_regex)

    @property
    def sound(self):
        if self.match_pattern(self.orig_word, self.sound_regex) is None:
            return ''
        return self.match_pattern(self.orig_word, self.sound_regex)

    @property
    def vowel(self):
        # [REP] will be used for conversion to Lu/Ru
        return self.orig_word.replace(self.sound, '').replace(self.start, '[REP]', 1)
#     def vowel(self):
#         return self.orig_word.replace(self.sound,'').replace(self.end,'').replace(self.start,'[REP]',1) #[REP] will be used for conversion to Lu/Ru

    @property  # might not need this one in final application as we need vowel
    def end(self):
        if self.match_pattern(self.vowel, self.end_regex) not in self.vowels_form:
            return self.match_pattern(self.vowel, self.end_regex)
        else:
            return None

#     # a setter function
#     @start.setter
#     def start(self):
#         print("setter method called")
#         self._start = match_pattern(self.start_regex)

    def match_pattern(self, text, regex_pattern):
        output_start = None
        if self.debug:
            print(text)
        for pattern in regex_pattern:
            matches = re.search(pattern, text, re.DOTALL)

            if matches is not None and self.debug:
                print(pattern, matches.group(1))
            if matches is not None:
                output_start = matches.group(1)
        return output_start

    def check_double_start_alphabets(self, text):
        '''Use to check in case starting alphabet is longer than one, 
        ref:https://sites.google.com/site/phasathaionline/hnwy-kar-reiyn-ru2/phyaychnatn'''
        # Function that check word in case like ขนม and else

        two_char = self.lead_char_nosound + self.two_char_combine

        max_lcs = 0
        if text in two_char:
            return text
        else:
            for char in two_char:
                if LCSubStr(text, char, len(text), len(char)) > max_lcs:
                    max_lcs = LCSubStr(text, char, len(text), len(char))
                    max_lcs_char = char
            return max_lcs_char

        return None

    def check_double_start_sound(self, text):
        '''Use to address the case where start alphabets are double and need to split to reflect actual pronunciation 
        ref:https://sites.google.com/site/phasathaionline/hnwy-kar-reiyn-ru2/phyaychnatn'''
        # Function that check word in case like ขนม and else

        return None

    def remove_karan(self, regex_pattern):
        return None
        # Write specific function for removing ์
