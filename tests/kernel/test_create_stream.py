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

from p4templates.kernel.create_stream import create_stream

class MockP4(object):
    def __init__(self, ):
        self.stream = {
            'Stream': '//depot_name/Existing',
            'Type': 'stream',
            'Owner': None,
            'ParentView': None,
            'Parent': None,
            'Paths': None,
            'Remapped': None,
            'Ignored': None,
            'Options': None
        }

        self.fetch_called = False
        self.save_called = False

    def iterate_streams(self):
        return [self.stream]

    def fetch_stream(self, stream_name):
        self.stream['Stream'] = stream_name
        self.fetch_called = True
        return self.stream

    def save_stream(self, stream_spec):
        self.stream = stream_spec
        self.save_called = True
        return self.stream


@pytest.mark.parametrize(
    'depot_name,stream_name,user_name,stream_type,parent_view,parent_stream,options,paths,remapped,ignored,dryrun,fetch_called,save_called,expected_stream',
    [
        ('depot_name', 'stream_name', 'user_name', 'mainline', 'parent_view', 'parent_stream', 'options', 'paths', 'remapped', 'ignored', False, True, True, {'Stream': '//depot_name/stream_name', 'Type': 'mainline', 'Owner': 'user_name', 'ParentView': 'parent_view', 'Parent': '//depot_name/parent_stream', 'Paths': 'paths', 'Remapped': 'remapped', 'Ignored': 'ignored', 'Options': 'options'}),
        ('depot_name', 'stream_name', 'user_name', 'mainline', 'parent_view', 'parent_stream', None, 'paths', 'remapped', 'ignored', False, True, True, {'Stream': '//depot_name/stream_name', 'Type': 'mainline', 'Owner': 'user_name', 'ParentView': 'parent_view', 'Parent': '//depot_name/parent_stream', 'Paths': 'paths', 'Remapped': 'remapped', 'Ignored': 'ignored', 'Options': 'allsubmit unlocked notoparent nofromparent mergedown'}),
        ('depot_name', 'stream_name', 'user_name', 'development', 'parent_view', 'parent_stream', 'options', 'paths', 'remapped', 'ignored', True, True, False, {'Stream': '//depot_name/stream_name', 'Type': 'development', 'Owner': 'user_name', 'ParentView': 'parent_view', 'Parent': '//depot_name/parent_stream', 'Paths': 'paths', 'Remapped': 'remapped', 'Ignored': 'ignored', 'Options': 'options'}),
        ('depot_name', 'stream_name', 'user_name', 'development', 'parent_view', 'none', 'options', 'paths', 'remapped', 'ignored', False, True, False, {'Stream': '//depot_name/stream_name', 'Type': 'development', 'Owner': 'user_name', 'ParentView': 'parent_view', 'Parent': 'none', 'Paths': 'paths', 'Remapped': 'remapped', 'Ignored': 'ignored', 'Options': 'options'}),
        ('depot_name', 'stream_name', 'user_name', 'development', 'parent_view', 'parent_stream', None, 'paths', 'remapped', 'ignored', True, True, False, {'Stream': '//depot_name/stream_name', 'Type': 'development', 'Owner': 'user_name', 'ParentView': 'parent_view', 'Parent': '//depot_name/parent_stream', 'Paths': 'paths', 'Remapped': 'remapped', 'Ignored': 'ignored', 'Options': 'allsubmit unlocked toparent fromparent mergedown'}),
        ('depot_name', 'Existing', 'user_name', 'mainline', 'parent_view', 'parent_stream', 'options', 'paths', 'remapped', 'ignored', False, False, False, {'Stream': '//depot_name/Existing', 'Type': 'stream', 'Owner': None, 'ParentView': None, 'Parent': None, 'Paths': None, 'Remapped': None, 'Ignored': None, 'Options': None}),
    ]
)
def test_create_stream(depot_name, stream_name, user_name, stream_type, parent_view, parent_stream, options, paths, remapped, ignored, dryrun, fetch_called, save_called, expected_stream):
    m_server = MockP4()

    create_stream(m_server, depot_name, stream_name, user_name, stream_type, parent_view, parent_stream, options, paths, remapped, ignored, dryrun)

    assert m_server.stream == expected_stream
    assert m_server.fetch_called == fetch_called
    assert m_server.save_called == save_called
