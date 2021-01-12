import pytest
from typing import NamedTuple, Optional, List
from kampuan.const import REP


class TestWord(NamedTuple):
    raw: str
    vowel_form: Optional[str] = None
    init_consonant: Optional[str] = None
    final_consonant: Optional[str] = None
    tone_mark: Optional[str] = None
    # all_consonants: Optional[List[str]]=None


words_list = [

    ('กำ', '-ำ', 'ก', None, None),
    ('ใคร', 'ใ-', 'คร', None, None),
    ('เขียว', 'เ-ีย', 'ข', 'ว', None),
    ('เกรียน', 'เ-ีย', 'กร', 'น', None),
    ('ปลอม', '-อ', 'ปล', 'ม', None),
    ('กลบ', '-', 'กล', 'บ', None),
    ('ตด', '-', 'ต', 'ด', None),
    ('นอน', '-อ', 'น', 'น', None),
    ('ขนุน', '-ุ', 'ขน', 'น', None),
    ('จัง', '-ั', 'จ', 'ง', None),
    ('คั่ว', '-ัว', None, None, '่'),
    ('ตู่', '-ู',  'ต', None, '่',),
    ('ใหญ่', 'ใ-', 'หญ', None, '่',),
    ('เดา', 'เ-า', 'ด', None, None),
    ('เปรต', 'เ-', 'ปร', 'ต', None),
    ('เสร็จ', 'เ-็', 'สร', 'จ', None),
    ('ปีน', '-ี', 'ป', 'น', None),
    ('เปี๊ยะ', 'เ-ียะ', 'ป', None, '๊'),
    ('คั่ว', '-ัว', None, None, '่'),
    ('แก้ม', 'แ-', 'ก', 'ม', '้'),
    ('แช่ง', 'แ-', 'ช', 'ง', '่'),
    ('แกล้ม', 'แ-', 'กล', 'ม', '้'),
    ('แพร่', 'แ-', 'พร', None, '่'),
    ('แข็ง', 'แ-็', 'ข', 'ง', None),
    ('เกลอ', 'เ-อ', 'กล', None, None),
    ('เทอญ', 'เ-อ', 'ท', 'ญ', None),
    ('เกิด', 'เ-ิ', 'ก', 'ด', None),
    ('เตลิด', 'เ-ิ', 'ตล', 'ด', None),
    ('กลม', '-', 'กล', 'ม', None),
    ('เลว', 'เ-', 'ล', 'ว', None),
    ('เสก', 'เ-', 'ส', 'ก', None),
    ('วัว', '-ัว', 'ว', None, None),
    ('เยี่ยม', 'เ-ีย', 'ย', 'ม', '่'),
    ('เพลง', 'เ-', 'พล', 'ง', None),
    ('ปลอม', '-อ', 'ปล', 'ม', None),
    ('หอม', '-อ', 'ห', 'ม', None),
    ('เวร', 'เ-', 'ว', 'ร', None),
    ('อย่าง', '-า', 'อย', 'ง', '่'),
    ('อยู่', '-ู', 'อย', None, '่'),
    ('อย่า', '-า', 'อย', None, '่'),
    ('กวน', '-ว', 'ก', 'น', None),
    ('แวว', 'แ-', 'ว', 'ว', None),
    ('วน', '-', 'ว', 'น', None),
    ('ว่าย', '-า', 'ว', 'ย', None),
    ('สวย', '-ว', 'ส', 'ย', None),
    ('เขย', 'เ-', 'ข', 'ย', None),
    ('เกรง', 'เ-', 'กร', 'ง', None),
    ('แปลง', 'แ-', 'ปล', 'ง', None),
    ('กรง', '-', 'กร', 'ง', None),
    ('ธง', '-', 'ธ', 'ง', None),
    ('ครี่', '-ี', 'คร', None, '่'),
    ('แซง', 'แ-', 'ซ', 'ง', None),
    ('แปล', 'แ-', 'ปล', None, None),
    ('แทรก', 'แ-', 'ทร', 'ก', None),
    ('ท้อ', '-อ', 'ท', None, '้'),
    ('ท้อง', '-อ', 'ท', 'ง', '้'),
    ('ใคร', 'ใ-', 'คร', None, None),
    ('เสวย', 'เ-', 'สว', 'ย', None),
    ('บรรณ', '-', 'บรร', 'ณ', None),
    ('สมุทร', '-ุ', 'สม', 'ทร', None),
    ('จันทร์', '-ั', 'จ', 'น', None),
    ('พันธุ์', '-ั', 'พ', 'น', None),
    ('กริบ', '-ิ', 'กร', 'บ', None),
    ('อยาก', '-า', 'อย', 'ก', None),
    ('กบ', '-', 'ก', 'บ', None),
    ('เกษม', 'เ-', 'กษ', 'ม', None),
    ('เออ', 'เ-อ', 'อ', None, None),
    ('มอ', '-อ', 'ม', None, None)
]
words_list = [TestWord(*item) for item in words_list]


@ pytest.fixture(scope='module', params=words_list)
def words(request):
    yield request.param


# Example fixture to test list
@ pytest.fixture(scope='module', params=[1, 2, 3])
def numbers(request):
    yield request.param
