#    p4templates - custom tooling to quickly create Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2024 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

from p4templates.kernel.utils import (
    load_server_config,
    setup_server_connection,
    set_default,
    write_json,
    read_json,
    validate_json,
    gather_parameters,
    substitute_parameters,
    convert_to_string,
    gather_existing_template_names,
)

def mock_read(value):
    if value == 'fail':
        raise Exception()
    return {'yep':'good'}


class MockP4(object):
    def __init__(
        self,
    ):
        self.charset = None
        self.password = None
        self.user = None
        self.port = None
        self.connect_called = False
        self.run_login_called = False

    def connect(self):
        self.connect_called = True

    def run_login(self):
        self.run_login_called = True


def test_load_server_config(mocker):
    m_read_json = mocker.patch("p4templates.kernel.utils.read_json")
    m_validate_json = mocker.patch("p4templates.kernel.utils.validate_json", return_value=True)

    load_server_config("a/fake/config/path.json")

    m_validate_json.assert_called_once_with("a/fake/config/path.json")
    m_read_json.assert_called_once_with("a/fake/config/path.json")
    


@pytest.mark.parametrize(
    "port,user,password,charset,connect_called,run_login_called",
    [
        ("port", "user", "password", "charset", True, True),
        ("port", "user", None, "charset", True, False),
        (None, "user", "password", "charset", False, False),
        ("port", None, "password", "charset", False, False),
    ],
)
def test_setup_server_connection(
    mocker, port, user, password, charset, connect_called, run_login_called
):
    mocker.patch("p4templates.kernel.utils.P4", return_value=MockP4())
    p4_connection = setup_server_connection(port, user, password, charset)

    if not connect_called and not run_login_called:
        assert p4_connection == None
    else:
        assert p4_connection.port == port
        assert p4_connection.user == user
        assert p4_connection.password == password
        assert p4_connection.charset == charset
        assert p4_connection.connect_called == connect_called
        assert p4_connection.run_login_called == run_login_called


def test_set_default():
    test_set = {1, 2, 3}
    test_list = [1, 2, 3]

    set_result = set_default(test_set)
    list_result = set_default(test_list)

    assert isinstance(set_result, list)
    assert isinstance(list_result, list)
    assert set_result == test_list
    assert list_result == test_list


def test_write_json(mocker):
    m_open = mocker.patch(
        "p4templates.kernel.utils.open", mocker.mock_open(read_data="{'fake':'data'}")
    )
    m_json_dump = mocker.patch("p4templates.kernel.utils.json.dump")

    write_json({"fake": "data"}, "/a/fake/output/path.json")

    m_open.assert_called_once_with("/a/fake/output/path.json", "w")
    m_json_dump.assert_called_once_with(
        {"fake": "data"},
        m_open.return_value,
        default=set_default,
        indent=4,
        sort_keys=False,
    )


def test_read_json(mocker):
    m_open = mocker.patch(
        "p4templates.kernel.utils.open", mocker.mock_open(read_data="{'fake':'data'}")
    )
    m_json_load = mocker.patch("p4templates.kernel.utils.json.load", return_value= {'fake':'data'})

    read_json("/a/fake/output/path.json")

    m_open.assert_called_once_with("/a/fake/output/path.json")
    m_json_load.assert_called_once_with(m_open.return_value)


@pytest.mark.parametrize(
    "read_value,expected_result",
    [
        ('a/fake/json/path.json', True),
        ('fail', False),
    ],
)
def test_validate_json(mocker, read_value, expected_result):
    mocker.patch('p4templates.kernel.utils.read_json', mock_read)
    
    result = validate_json(read_value)
    
    assert result == expected_result


def test_gather_parameters():
    test_dict = {'name': r"{template}_{parameter}"}
    result = gather_parameters(test_dict)
    assert result == ['parameter', 'template']


def test_substitute_parameters():
    test_dict = {'name': r"{template}_{parameter}"}
    test_replacements = {'template': 'all', 'parameter': 'good'}
    result = substitute_parameters(test_dict, test_replacements)
    assert result == {'name': "all_good"}

@pytest.mark.parametrize(
        'input,expected_result',
        [
            (1,'1'),
            (1.0,'1.0'),
            ('string','string'),
            (['list','string'],'list string'),
            ({'set', 'string'},'set string'),
            (('tuple','string'),'tuple string'),
        ]
)
def test_convert_to_string(input, expected_result):
    assert convert_to_string(input) == expected_result


def test_gather_existing_template_names(mocker):
    m_os_path_isdir = mocker.patch('p4templates.kernel.utils.os.path.isdir', return_value=True)
    m_os_walk = mocker.patch('p4templates.kernel.utils.os.walk', return_value=[('a/fake/root/', ('a/fake/dir',), ('fake.json',)),])
    m_read_json = mocker.patch('p4templates.kernel.utils.read_json', return_value={'name':'demo'})
    m_validate_json = mocker.patch('p4templates.kernel.utils.validate_json', return_value=True)
    
    expected_result = {'demo': 'a/fake/root/fake.json'}

    result = gather_existing_template_names()

    assert result == expected_result