from kampuan.const import THAI_CHARS, THAI_CONS, THAI_VOW, THAI_TONE


def test_const():
    assert len(THAI_CHARS) == 88
    assert len(THAI_CONS) == 44
    assert len(THAI_VOW) == 20
    assert len(THAI_TONE) == 4


def test_numbers(numbers):
    assert numbers < 5
