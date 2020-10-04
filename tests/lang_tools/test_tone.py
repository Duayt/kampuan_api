from kampuan.lang_tools import remove_tone_mark


def test_remove_tone_mark():

    assert remove_tone_mark('ไก่') == 'ไก'
    assert remove_tone_mark('ใกล้') == 'ใกล'
    assert remove_tone_mark('เจ๊ง') == 'เจง'
    assert remove_tone_mark('เจ๋ง') == 'เจง'