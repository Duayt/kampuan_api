from kampuan.lang_tools import handle_white_spaces, process_555


def test_handle_white_spaces():
    assert handle_white_spaces('สวัส ดี') == 'สวัส,ดี'
    assert handle_white_spaces('สะ วัส  ดี ') == 'สะ,วัส,ดี,'


def test_process_555():
    assert process_555('สวัสดี555') == 'สวัสดีฮ่าฮ่าฮ่า'


