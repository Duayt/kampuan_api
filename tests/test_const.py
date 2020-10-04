from kampuan.const import *


def test_const():
    assert len(THAI_CHARS) == 88
    assert len(THAI_CONS) == 44
    assert len(THAI_VOW) == 20
    assert len(THAI_TONE) == 4
