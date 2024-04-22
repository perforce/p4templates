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
from  p4templates.p4templates_tool import main
from collections import namedtuple

args_tuple = namedtuple('ArgsTuple', ['config', 'template_dir'])

class MockArgumentParser(object):
    def __init__(self, args_dict=None):
        self.args_dict = args_dict or {}

    def add_argument(
        self, short_name, long_name, default=None, nargs=None, action=None
    ):
        pass

    def parse_args(self):
        return self.args_dict


@pytest.mark.parametrize(
    "given_args,config_values,dir_exists_values",
    [
        (args_tuple('config', 'template_dir'), {'template_dir': 'template_dir'}, [True, True]),
        (args_tuple('config', 'template_dir'), {'template_dir': ''}, [True, True]),
        (args_tuple('config', 'template_dir'), {'template_dir': 'template_dir'}, [True, False]),
        (args_tuple('config', 'template_dir'), {'template_dir': 'template_dir'}, [False, False]),
    ],
)
def test_main(mocker, given_args, config_values, dir_exists_values):
    m_ArgumentParser = mocker.patch("p4templates.p4templates_tool.ArgumentParser", return_value=MockArgumentParser(given_args))
    m_os_path_exists = mocker.patch("p4templates.p4templates_tool.os.path.exists", side_effect=dir_exists_values)
    m_os_path_abspath = mocker.patch("p4templates.p4templates_tool.os.path.abspath", return_value='abs_path')
    m_load_server_config = mocker.patch("p4templates.p4templates_tool.load_server_config", return_value=config_values)
    m_os_path_dirname = mocker.patch("p4templates.p4templates_tool.os.path.dirname", return_value='a/dir/name/')
    m_os_chdir = mocker.patch("p4templates.p4templates_tool.os.chdir")
    m_QApplication = mocker.patch("p4templates.p4templates_tool.QApplication")
    m_P4TemplateLoaderDialog = mocker.patch("p4templates.p4templates_tool.P4TemplateLoaderDialog")

    main()

    path_exists_calls = [
        mocker.call('config'),
        mocker.call('template_dir')
    ]

    abspath_calls = [
        mocker.call('config'),
        mocker.call('template_dir')
    ]

    path_dirname_calls = [
        mocker.call('nope')
    ]

    m_ArgumentParser.assert_called_once()
    m_os_path_exists.assert_has_calls(path_exists_calls)
    if dir_exists_values[0] and dir_exists_values[1]:
        m_os_path_abspath.assert_has_calls(abspath_calls)
        m_load_server_config.assert_called_once_with('abs_path')
    m_os_path_dirname.assert_called_once()
    m_os_chdir.assert_called_once()
    m_QApplication.assert_called_once()
    if dir_exists_values[0] and dir_exists_values[1]:
        m_P4TemplateLoaderDialog.assert_called_once_with(config_path='abs_path', template_dir='abs_path')
    elif dir_exists_values[0]:
        m_P4TemplateLoaderDialog.assert_called_once_with(config_path='abs_path', template_dir='template_dir')
    else:
        m_P4TemplateLoaderDialog.assert_called_once_with(config_path='config', template_dir='template_dir')
