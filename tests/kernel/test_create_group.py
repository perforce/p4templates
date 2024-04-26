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

from p4templates.kernel.create_group import create_group

class MockP4(object):
    def __init__(self, ):
        self.group = {
            'Group': 'Existing',
            'Description': None,
            'MaxResults': None,
            'MaxScanRows': None,
            'MaxLockTime': None,
            'MaxOpenFiles': None,
            'MaxMemory': None,
            'Timeout': None,
            'PasswordTimeout': None,
            'Subgroups': None,
            'Owners': None,
            'Users': None,
        }

        self.fetch_called = 0
        self.save_called = 0

    def iterate_groups(self):
        return [self.group]

    def fetch_group(self, group_name):
        self.group['Group'] = group_name
        self.fetch_called = 1
        return self.group

    def save_group(self, group_spec):
        self.group = group_spec
        self.save_called = 1
        return self.group




@pytest.mark.parametrize(
    'group_name,description,max_results,max_scan_rows,max_lock_time,max_open_files,max_memory,timeout,password_timeout,subgroups,owners,users,dryrun,fetch_called,save_called,expected_group',
    [
        ('group_name', 'description', 'max_results', 'max_scan_rows', 'max_lock_time', 'max_open_files', 'max_memory', 'timeout', 'password_timeout', 'subgroups', 'owners', 'users', False, True, True, {'Group': 'group_name', 'Description': 'description', 'MaxResults': 'max_results', 'MaxScanRows': 'max_scan_rows', 'MaxLockTime': 'max_lock_time', 'MaxOpenFiles': 'max_open_files', 'MaxMemory': 'max_memory', 'Timeout': 'timeout', 'PasswordTimeout': 'password_timeout', 'Subgroups': 'subgroups', 'Owners': 'owners', 'Users': 'users'}),
        ('group_name', 'description', 'max_results', 'max_scan_rows', 'max_lock_time', 'max_open_files', 'max_memory', 'timeout', 'password_timeout', 'subgroups', 'owners', 'users', True, True, False, {'Group': 'group_name', 'Description': 'description', 'MaxResults': 'max_results', 'MaxScanRows': 'max_scan_rows', 'MaxLockTime': 'max_lock_time', 'MaxOpenFiles': 'max_open_files', 'MaxMemory': 'max_memory', 'Timeout': 'timeout', 'PasswordTimeout': 'password_timeout', 'Subgroups': 'subgroups', 'Owners': 'owners', 'Users': 'users'}),
        ('Existing', 'description', 'max_results', 'max_scan_rows', 'max_lock_time', 'max_open_files', 'max_memory', 'timeout', 'password_timeout', 'subgroups', 'owners', 'users', False, False, False, {'Group': 'Existing', 'Description': None, 'MaxResults': None, 'MaxScanRows': None, 'MaxLockTime': None, 'MaxOpenFiles': None, 'MaxMemory': None, 'Timeout': None, 'PasswordTimeout': None, 'Subgroups': None, 'Owners': None, 'Users': None}),
    ]
)
def test_create_group(group_name, description, max_results, max_scan_rows, max_lock_time, max_open_files, max_memory, timeout, password_timeout, subgroups, owners, users, dryrun, fetch_called, save_called, expected_group):
    m_server = MockP4()

    create_group(m_server, group_name, description, max_results, max_scan_rows, max_lock_time, max_open_files, max_memory, timeout, password_timeout, subgroups, owners, users, dryrun)

    assert m_server.group == expected_group
    assert m_server.fetch_called == fetch_called
    assert m_server.save_called == save_called
