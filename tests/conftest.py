import pytest
from typing import NamedTuple, Optional, List
from kampuan.const import REP


class TestWord(NamedTuple):
    raw: str
    vowel_form: Optional[str] = None
    tone_mark: Optional[str] = None
    init_consonant: Optional[str] = None
    final_consonant: Optional[str] = None
    # all_consonants: Optional[List[str]]=None


words_list = [
    TestWord('เขียว', 'เ-ีย', None, 'ข', 'ว'),
    TestWord('เกรียน', 'เ-ีย', None, 'กร', 'น'),
    TestWord('ตู่', '-ู', '-่', 'ต', None),
    TestWord('คั่ว', '-ัว', '-่', None, None),
    TestWord('ปลอม', '-อ', None, 'ปล', 'ม'),
    TestWord('กลบ', '-', None, 'กล', 'บ'),
]


@pytest.fixture(scope='module', params=words_list)
def words(request):
    yield request.param


# Example fixture to test list
@pytest.fixture(scope='module', params=[1, 2, 3])
def numbers(request):
    yield request.param
