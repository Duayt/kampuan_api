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
]


@pytest.fixture(scope='module', params=words_list)
def test_words(request):
    yield request


# @ pytest.mark.parametrize(
#     'test_word',
#     (['เขียว', 'เ-ีย', None, 'ข', 'ว'],
#      ['เกรียน', 'เ-ีย', None, 'กร', 'น']),
#     indirect = True
# )
