import pytest
from kampuan.lang_tools import (handle_white_spaces, insert_ch_after,
                                normalize_word, process_555, process_double,
                                process_num_to_thaiword, process_text_2_list,
                                remove_tone_mark)


def test_handle_white_spaces():
    assert handle_white_spaces('สวัส ดี') == 'สวัส,ดี'
    assert handle_white_spaces('สะ วัส  ดี ') == 'สะ,วัส,ดี,'


def test_process_555():
    assert process_555(['สวัสดี', '555']) == ['สวัสดี', 'ฮ่า', 'ฮ่า', 'ฮ่า']
    assert process_555(['กิน', '5', 'มื้อ']) == ['กิน', '5', 'มื้อ']
    assert process_555(['5555', 'ตลก']) == ['ฮ่า', 'ฮ่า', 'ฮ่า', 'ฮ่า', 'ตลก']


def test_normalized_word():
    assert normalize_word('เเปลก') == 'แปลก'


@ pytest.mark.parametrize("text_with_nums, expected_result", [
    (0, ['ศูนย์']),
    (1, ['หนึ่ง']),
    (2, ['สอง']),
    (3, ['สาม']),
    (4, ['สี่']),
    (5, ['ห้า']),
    (6, ['หก']),
    (7, ['เจ็ด']),
    (8, ['แปด']),
    (9, ['เก้า']),
])
def test_num_to_thai(text_with_nums, expected_result):
    assert process_num_to_thaiword(str(text_with_nums)) == expected_result


def test_insert_ch_after():
    assert insert_ch_after('ทดสอบนำจ้า', '้', 5) == 'ทดสอบน้ำจ้า'
    assert insert_ch_after('0123456', 'a', 0) == '0a123456'
    assert insert_ch_after('0123456', 'a', 6) == '0123456a'


def test_process_double():
    assert process_double(['ได้', 'ๆ', 'ไป', 'กิน', 'บ่อย', 'ๆ', 'ๆ']) == [
        'ได้', 'ได้', 'ไป', 'กิน', 'บ่อย', 'บ่อย', 'บ่อย']


def test_process_text_2_list():
    assert process_text_2_list('ว่า ยัง ไง ละ ครับ') == [
        'ว่า', 'ยัง', 'ไง', 'ละ', 'ครับ']
    assert process_text_2_list('a   b c   de') == ['a', 'b', 'c', 'de']


@ pytest.mark.parametrize("before_remove_tone, removed_tone", [
    ('ไก่', 'ไก'),
    ('ได้', 'ได'),
    ('ไป๊', 'ไป'),
    ('อู๋', 'อู'),
    ('เป็ด', 'เป็ด'),
])
def test_remove_tone_mark(before_remove_tone, removed_tone):
    assert remove_tone_mark(before_remove_tone) == removed_tone
