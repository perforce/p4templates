import pytest

from p4templates.kernel.edit_typemap import (
    get_typemap,
    add_type,
    save_typemap,
    append_new_typemap_entry,
)


class MockP4(object):
    def __init__(
        self,
    ):
        self.typemap = {
            "TypeMap": ["text //....py"]
        }

        self.fetch_called = 0
        self.save_called = 0


    def fetch_typemap(self):
        self.fetch_called = 1
        return self.typemap

    def save_typemap(self, typemap_spec):
        self.typemap = typemap_spec
        self.save_called = 1
        return [self.typemap]


def test_get_typemap():
    m_server = MockP4()
    
    expected_result = {"text": {'//....py'}}
    
    result = get_typemap(m_server)

    assert result == expected_result


def test_add_type():
    type_dict = {}
    expected_result = {"text": {'//....py'}}
    
    result = add_type(type_dict, 'text', '//....py')

    assert result == expected_result


@pytest.mark.parametrize(
    'dryrun,expected_result',
    [
        (True, {"TypeMap": ["text //....py"]}),
        (False, {"TypeMap": ["text //....py", "text //....txt"]})
    ]
)
def test_save_typemap(dryrun, expected_result):
    m_server = MockP4()
    type_dict = {"text": {'//....py', '//....txt'}} 

    save_typemap(type_dict, m_server, dryrun)

    assert m_server.save_called != dryrun
    assert m_server.typemap == expected_result


def test_append_new_typemap_entry(mocker):
    m_server = MockP4()
    m_get_typemap = mocker.patch('p4templates.kernel.edit_typemap.get_typemap')
    m_add_type = mocker.patch('p4templates.kernel.edit_typemap.add_type')
    m_save_typemap = mocker.patch('p4templates.kernel.edit_typemap.save_typemap')

    append_new_typemap_entry({"text": {'//....py'}}, m_server)

    m_get_typemap.assert_called_once_with(m_server)
    m_add_type.assert_called_once_with(m_get_typemap.return_value, 'text', '//....py')
    m_save_typemap.assert_called_once_with(m_add_type.return_value, m_server, 0)

