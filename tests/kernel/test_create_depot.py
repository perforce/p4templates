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

from p4templates.kernel.create_depot import create_depot

class MockP4(object):
    def __init__(self, ):
        self.depot = {
            'Depot': 'Existing',
            'Type': 'stream',
            'StreamDepth': '//Existing/1'
        }

        self.fetch_called = 0
        self.save_called = 0

    def iterate_depots(self):
        return [self.depot]

    def fetch_depot(self, depot_name):
        self.depot['Depot'] = depot_name
        self.depot['StreamDepth'] = '//{}/1'.format(depot_name)
        self.fetch_called = 1
        return self.depot

    def save_depot(self, depot_spec):
        self.depot = depot_spec
        self.save_called = 1
        return self.depot


@pytest.mark.parametrize(
    'name,type,depth,dryrun,fetch_called,save_called,expected_depot',
    [
        ('test_depot','stream', 1, False, True, True, {'Depot': 'test_depot', 'Type': 'stream', 'StreamDepth': '//test_depot/1'}),
        ('Existing','stream', 1, False, False, False, {'Depot': 'Existing', 'Type': 'stream', 'StreamDepth': '//Existing/1'}),
        ('test_depot','stream', 1, True, True, False, {'Depot': 'test_depot', 'Type': 'stream', 'StreamDepth': '//test_depot/1'}),
    ]
)
def test_create_depot(name, type, depth, dryrun, fetch_called, save_called, expected_depot):
    m_server = MockP4()

    create_depot(m_server, name, type, depth, dryrun)

    assert m_server.depot == expected_depot
    assert m_server.fetch_called == fetch_called
    assert m_server.save_called == save_called
