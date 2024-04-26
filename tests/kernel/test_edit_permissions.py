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

from p4templates.kernel.edit_permissions import (
    get_protections_table,
    validate_protection,
    prepend_protection,
    save_protections_table,
    append_new_protections,
)


class MockP4(object):
    def __init__(
        self,
    ):
        self.protect = {
            "Protections": ["access type name host path  ## comment", "broken"]
        }

        self.fetch_called = 0
        self.save_called = 0

    def fetch_protect(self):
        self.fetch_called = 1
        return self.protect

    def save_protect(self, protect_spec):
        self.protect = protect_spec
        self.save_called = 1
        return [self.protect]


def test_get_protections_table():
    m_server = MockP4()

    expected_result = [
        {
            "access": "access",
            "type": "type",
            "name": "name",
            "host": "host",
            "path": "path",
            "comment": "comment",
        }
    ]

    result = get_protections_table(m_server)
    print(result)
    assert result == expected_result


@pytest.mark.parametrize(
    "protection,expected_result",
    [
        (
            {
                "access": "access",
                "type": "type",
                "name": "name",
                "host": "host",
                "path": "path",
                "comment": "comment",
            },
            True,
        ),
        ({"type": "type", "name": "name", "host": "host", "path": "path"}, False),
        ({"access": "access", "name": "name", "host": "host", "path": "path"}, False),
        ({"access": "access", "type": "type", "host": "host", "path": "path"}, False),
        ({"access": "access", "type": "type", "name": "name", "path": "path"}, False),
        ({"access": "access", "type": "type", "name": "name", "host": "host"}, False),
    ],
)
def test_validate_protection(protection, expected_result):
    result = validate_protection(protection)
    assert result == expected_result


def test_prepend_protection():
    protection = 'protection'
    protection_table = ['existing']
    expected_result = ['protection', 'existing']

    result = prepend_protection(protection_table, protection)

    assert result == expected_result

    result = prepend_protection(protection_table, protection)

    assert result == expected_result


@pytest.mark.parametrize(
    "protection_table,dryrun,expected_result",
    [
        (   [
                {
                    "access": "access",
                    "type": "type",
                    "name": "name",
                    "host": "host",
                    "path": "path",
                    "comment": "comment",
                }
            ],
            True,
            {'Protections': ['access type name host path  ## comment', 'broken']}
        ),
        (   [
                {
                    "access": "access",
                    "type": "type",
                    "name": "name",
                    "host": "host",
                    "path": "path",
                    "comment": "comment",
                }
            ],
            False,
            {'Protections': ['access type name host path ## comment']}
        ),
    ]
)
def test_save_protections_table(protection_table, dryrun, expected_result):
    m_server = MockP4()

    save_protections_table(protection_table, m_server, dryrun)

    assert m_server.protect == expected_result


def test_append_new_protections(mocker):
    m_server = MockP4()
    m_get_protections_table = mocker.patch('p4templates.kernel.edit_permissions.get_protections_table', return_value='existing_protection')
    m_validate_protection = mocker.patch('p4templates.kernel.edit_permissions.validate_protection', return_value=True)
    m_prepend_protection = mocker.patch('p4templates.kernel.edit_permissions.prepend_protection', return_value=['existing_protection', 'new_protection'])
    m_save_protections_table = mocker.patch('p4templates.kernel.edit_permissions.save_protections_table')

    new_protections = ['new_protection']

    append_new_protections(new_protections, m_server)

    m_get_protections_table.assert_called_once_with(m_server)
    m_validate_protection.assert_called_once_with(new_protections[0])
    m_prepend_protection.assert_called_once_with(m_get_protections_table.return_value, new_protections[0])
    m_save_protections_table.assert_called_once_with(m_prepend_protection.return_value, m_server, 0)
