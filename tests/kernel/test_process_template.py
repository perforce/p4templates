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
from collections import namedtuple
from p4templates.kernel.process_template import (
    process_template,
    get_template_preset,
    main,
)

args_tuple = namedtuple('ArgsTuple', ['dryrun', 'template', 'name', 'parameters', 'config'])


class MockP4(object):
    def __init__(self):
        pass


class MockArgumentParser(object):
    def __init__(self, args_dict=None):
        self.args_dict = args_dict or {}

    def add_argument(
        self, short_name, long_name, default=None, nargs=None, action=None
    ):
        pass

    def parse_args(self):
        return self.args_dict

    def set_args(self, args_dict=None):
        self.args_dict = args_dict or {}


@pytest.mark.parametrize(
    "dry_run",
    [
        (True),
        (False),
    ],
)
def test_process_template(mocker, dry_run):
    m_append_new_typemap_entry = mocker.patch(
        "p4templates.kernel.process_template.append_new_typemap_entry"
    )
    m_append_new_protections = mocker.patch(
        "p4templates.kernel.process_template.append_new_protections"
    )
    m_create_user = mocker.patch("p4templates.kernel.process_template.create_user")
    m_create_depot = mocker.patch("p4templates.kernel.process_template.create_depot")
    m_create_group = mocker.patch("p4templates.kernel.process_template.create_group")
    m_create_stream = mocker.patch("p4templates.kernel.process_template.create_stream")
    m_create_branch = mocker.patch("p4templates.kernel.process_template.create_branch")
    m_populate_branch = mocker.patch(
        "p4templates.kernel.process_template.populate_branch"
    )
    m_delete_branch = mocker.patch("p4templates.kernel.process_template.delete_branch")
    m_server = MockP4()

    template = {
        "name": "default_unreal_template",
        "depots": [{"name": "{project}_depot", "type": "stream", "depth": "1"}],
        "groups": [
            {
                "name": "{project}_group",
                "description": "A group I'll be making and deleting often.",
                "max_results": "unset",
                "max_scan_rows": "unset",
                "max_lock_time": "unset",
                "max_open_files": "unset",
                "timeout": "43200",
                "password_timeout": "unset",
                "subgroups": "",
                "owners": ["test_dude"],
                "users": ["test_dude"],
            }
        ],
        "users": [
            {"name": "test_dude", "email": "test1@dude.com", "full_name": "test dude"}
        ],
        "streams": [
            {
                "depot": "{project}_depot",
                "name": "{project}_main",
                "type": "mainline",
                "ignored": [
                    "*.pyc",
                    "/Intermediate/...",
                    "/Saved/...",
                    "/DerivedDataCache/...",
                    "/Build/...",
                ],
            }
        ],
        "protections": [
            {
                "access": "write",
                "type": "group",
                "name": "{project}_group",
                "host": "*",
                "path": "//{project}_depot/...",
                "comment": "auto generated",
            }
        ],
        "types": {
            "text": ["//....py"],
        },
        "branches": [
            {
                "name": "{project}_populate",
                "options": ["unlocked"],
                "view": {
                    "//populate_demo/main/old_project/...": "//{project}_depot/{project}_main/{project}/...",
                    "//populate_demo/main/old_project/old_project.py": "//{project}_depot/{project}_main/{project}/{project}.py",
                },
            }
        ],
        'post_config_message': 'post_config_message',
    }

    process_template(template, m_server, dry_run)

    m_append_new_typemap_entry.assert_called_once_with(
        {"text": ["//....py"]}, m_server, dryrun=dry_run
    )
    m_append_new_protections.assert_called_once_with(
        [
            {
                "access": "write",
                "type": "group",
                "name": "{project}_group",
                "host": "*",
                "path": "//{project}_depot/...",
                "comment": "auto generated",
            }
        ],
        m_server,
        dryrun=dry_run,
    )
    m_create_user.assert_called_once_with(
        m_server,
        name="test_dude",
        email="test1@dude.com",
        full_name="test dude",
        job_view=None,
        auth_method=None,
        reviews=None,
        dryrun=dry_run,
    )
    m_create_depot.assert_called_once_with(
        m_server,
        depot_name="{project}_depot",
        depot_type="stream",
        stream_depth="1",
        dryrun=dry_run,
    )
    m_create_group.assert_called_once_with(
        m_server,
        group_name="{project}_group",
        description="A group I'll be making and deleting often.",
        max_results="unset",
        max_scan_rows="unset",
        max_lock_time="unset",
        max_open_files="unset",
        max_memory=None,
        timeout="43200",
        password_timeout="unset",
        subgroups="",
        owners=["test_dude"],
        users=["test_dude"],
        dryrun=dry_run,
    )
    m_create_stream.assert_called_once_with(
        m_server,
        depot_name="{project}_depot",
        stream_name="{project}_main",
        stream_type="mainline",
        user_name=None,
        parent_view=None,
        parent_stream=None,
        options=None,
        paths=None,
        remapped=None,
        ignored=[
            "*.pyc",
            "/Intermediate/...",
            "/Saved/...",
            "/DerivedDataCache/...",
            "/Build/...",
        ],
        dryrun=dry_run,
    )
    m_create_branch.assert_called_once_with(
        m_server,
        branch_name="{project}_populate",
        view={
            "//populate_demo/main/old_project/...": "//{project}_depot/{project}_main/{project}/...",
            "//populate_demo/main/old_project/old_project.py": "//{project}_depot/{project}_main/{project}/{project}.py",
        },
        options=["unlocked"],
        owner=None,
        dryrun=dry_run,
    )
    if not dry_run:
        m_populate_branch.assert_called_once_with(m_server, "{project}_populate")
        m_delete_branch.assert_called_once_with(m_server, "{project}_populate")
    else:
        m_populate_branch.assert_not_called()
        m_delete_branch.assert_not_called()


def test_get_template_preset(mocker):
    m_gather_existing_template_names = mocker.patch(
        "p4templates.kernel.process_template.gather_existing_template_names",
        return_value={"template_name": "template_data"},
    )
    result = get_template_preset("template_name", "/a/fake/template/dir")
    expected_result = "template_data"

    m_gather_existing_template_names.assert_called_once_with("/a/fake/template/dir")
    assert result == expected_result


@pytest.mark.parametrize(
    "given_args",
    [
        args_tuple(True, "a/template/file/path.json", "template_name", ["key:value"], '/a/fake/config/path.json'),
        args_tuple(True, False, "template_name", ["key:value"], '/a/fake/config/path.json'),
        args_tuple(True, False, False, ["key:value"], '/a/fake/config/path.json'),
        args_tuple(True, False, 'template_name', [], '/a/fake/config/path.json'),
    ],
)
def test_main(mocker, given_args):
    m_get_template_preset = mocker.patch(
        "p4templates.kernel.process_template.get_template_preset", return_value="a/template/file/path.json"
    )
    m_os_path_isfile = mocker.patch(
        "p4templates.kernel.process_template.os.path.isfile", return_value=True
    )
    m_validate_json = mocker.patch(
        "p4templates.kernel.process_template.validate_json", return_value=True
    )
    m_read_json = mocker.patch("p4templates.kernel.process_template.read_json")
    m_gather_parameters = mocker.patch(
        "p4templates.kernel.process_template.gather_parameters", return_value={'key': 'value'}
    )
    m_substitute_parameters = mocker.patch(
        "p4templates.kernel.process_template.substitute_parameters"
    )
    m_setup_server_connection = mocker.patch(
        "p4templates.kernel.process_template.setup_server_connection"
    )
    m_load_server_config = mocker.patch(
        "p4templates.kernel.process_template.load_server_config", return_value={'server':{'config':'values'}}
    )
    m_process_template = mocker.patch(
        "p4templates.kernel.process_template.process_template"
    )
    mocker.patch(
        "p4templates.kernel.process_template.ArgumentParser",
        return_value=MockArgumentParser(given_args),
    )

    main()

    read_calls = [
        mocker.call("a/template/file/path.json"), 
        mocker.call().__bool__()
    ]

    if given_args.template or not given_args.name:
        m_get_template_preset.assert_not_called()
    else:
        m_get_template_preset.assert_called_once_with('template_name')

    if not (given_args.template or given_args.name):
        m_read_json.assert_not_called()
    else:
        m_read_json.assert_has_calls(read_calls)

    if not (given_args.template or given_args.name):
        m_gather_parameters.assert_not_called()
        m_substitute_parameters.assert_not_called()
        m_setup_server_connection.assert_not_called()
        m_load_server_config.assert_not_called()
        m_process_template.assert_not_called()
    elif not given_args.parameters:
        m_gather_parameters.assert_called_once_with(m_read_json.return_value)
        m_substitute_parameters.assert_not_called()
        m_setup_server_connection.assert_not_called()
        m_load_server_config.assert_not_called()
        m_process_template.assert_not_called()
    else:
        m_gather_parameters.assert_called_once_with(m_read_json.return_value)
        m_substitute_parameters.assert_called_once_with(m_read_json.return_value, {"key":"value"})
        m_setup_server_connection.assert_called_once_with(config='values')
        m_load_server_config.assert_called_once_with('/a/fake/config/path.json')
        m_process_template.assert_called_once_with(m_substitute_parameters.return_value, m_setup_server_connection.return_value,given_args.dryrun)
