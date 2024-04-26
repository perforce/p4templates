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
from p4templates.ui.p4_template_loader_gui import P4TemplateLoaderDialog

from PyQt6.QtWidgets import (
    QVBoxLayout,
)

def test_P4TemplateLoaderDialog_init(qtbot,mocker):
    m_create_ui_elements = mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    m_add_ui_elements_to_layout = mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    m_connect_ui = mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    m_set_window_settings = mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    m_reload_ui = mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    m_exec = mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    P4TLG = P4TemplateLoaderDialog()
    qtbot.addWidget(P4TLG)

    assert isinstance(P4TLG, P4TemplateLoaderDialog)
    m_create_ui_elements.assert_called_once()
    m_add_ui_elements_to_layout.assert_called_once()
    m_connect_ui.assert_called_once()
    m_set_window_settings.assert_called_once()
    m_reload_ui.assert_called_once()
    m_exec.assert_called_once()


def test_P4TemplateLoaderDialog_create_ui_elements(qtbot, mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_QComboBox = mocker.patch('p4templates.ui.p4_template_loader_gui.QComboBox')
    m_QPushButton = mocker.patch('p4templates.ui.p4_template_loader_gui.QPushButton')
    m_QTableWidget = mocker.patch('p4templates.ui.p4_template_loader_gui.QTableWidget')

    push_calls = [
        mocker.call('New'),
        mocker.call('Edit'),
        mocker.call('Run'),
        ]

    P4TLG = P4TemplateLoaderDialog()

    qtbot.addWidget(P4TLG)

    m_QComboBox.assert_called_once()
    m_QPushButton.assert_has_calls(push_calls)
    m_QTableWidget.assert_called_once()


def test_P4TemplateLoaderDialog_update_parameters_populated(qtbot, mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.gather_parameters', return_value=['test'])
    mocker.patch('p4templates.ui.p4_template_loader_gui.read_json', return_value='data')

    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_validate_parameters = mocker.patch.object(P4TemplateLoaderDialog, 'validate_parameters')

    P4TLG = P4TemplateLoaderDialog()
    qtbot.addWidget(P4TLG)

    P4TLG.template_cbox.addItem('template_name')
    P4TLG.existing_template_lut['template_name'] = ''
    P4TLG.gathered_parameters = {'test':"test"}

    P4TLG.update_parameters_table()
    print('P4TLG.parameter_table.rowCount()', P4TLG.parameter_table.rowCount())

    P4TLG.gathered_parameters = {}

    assert  P4TLG.gathered_parameters == {}

    P4TLG.update_parameters()
    valid_calls = [
        mocker.call(),
        mocker.call()
    ]

    assert P4TLG.gathered_parameters == {'test':""}
    m_validate_parameters.assert_has_calls(valid_calls)


def test_P4TemplateLoaderDialog_update_parameters_empty(qtbot, mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.gather_parameters', return_value=['test'])
    mocker.patch('p4templates.ui.p4_template_loader_gui.read_json', return_value='data')

    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_validate_parameters = mocker.patch.object(P4TemplateLoaderDialog, 'validate_parameters')

    P4TLG = P4TemplateLoaderDialog()
    qtbot.addWidget(P4TLG)

    P4TLG.template_cbox.addItem('template_name')
    P4TLG.existing_template_lut['template_name'] = ''
    P4TLG.gathered_parameters = {'test':"test"}

    # P4TLG.update_parameters_table()
    # print('P4TLG.parameter_table.rowCount()', P4TLG.parameter_table.rowCount())

    P4TLG.gathered_parameters = {}

    assert  P4TLG.gathered_parameters == {}

    P4TLG.update_parameters()

    assert P4TLG.gathered_parameters == {}
    m_validate_parameters.assert_called_once()


@pytest.mark.parametrize(
        'parameters,valid',
        [
            ({'fail': ' '}, False),
            ({'pass':'pass'}, True),
        ]
)
def test_P4TemplateLoaderDialog_validate_parameters(qtbot, mocker, parameters, valid):
    #mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    P4TLG = P4TemplateLoaderDialog()
    qtbot.addWidget(P4TLG)
    P4TLG.gathered_parameters = parameters

    P4TLG.validate_parameters()

    assert P4TLG.btn_run.isEnabled() == valid


def test_P4TemplateLoaderDialog_update_parameters_table(mocker, qtbot):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_gather_parameters = mocker.patch('p4templates.ui.p4_template_loader_gui.gather_parameters', return_value=['test'])
    m_read_json = mocker.patch('p4templates.ui.p4_template_loader_gui.read_json', return_value='data')
    m_validate_parameters = mocker.patch.object(P4TemplateLoaderDialog, 'validate_parameters')

    P4TLG = P4TemplateLoaderDialog()

    P4TLG.parameter_table.setRowCount(len(P4TLG.gathered_parameters))
    qtbot.addWidget(P4TLG)

    P4TLG.update_parameters_table() # Empty

    assert P4TLG.parameter_table.rowCount() == 0

    P4TLG.template_cbox.addItem('template_name')
    P4TLG.existing_template_lut['template_name'] = ''
    P4TLG.gathered_parameters = {'test':"test"}

    P4TLG.update_parameters_table() # initial Populate

    assert P4TLG.parameter_table.rowCount() == 1

    P4TLG.update_parameters_table() # Populated

    assert P4TLG.parameter_table.rowCount() == 1

    valid_calls = [
        mocker.call(),
        mocker.call(),
    ]

    read_calls = [
        mocker.call(''),
        mocker.call(''),
    ]

    gather_calls = [
        mocker.call('data'),
        mocker.call('data'),
    ]


    m_validate_parameters.assert_has_calls(valid_calls)
    m_read_json.assert_has_calls(read_calls)
    m_gather_parameters.assert_has_calls(gather_calls)


def test_P4TemplateLoaderDialog_update_template_combobox(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')
    m_gather_existing_template_names = mocker.patch('p4templates.ui.p4_template_loader_gui.gather_existing_template_names', return_value={'file1': 'path1', 'file2': 'path2'})


    P4TLG = P4TemplateLoaderDialog()
    P4TLG.template_dir = 'template_dir'

    assert P4TLG.template_cbox.count() == 0

    P4TLG.update_template_combobox()

    gather_calls = [
        mocker.call('template_dir')
    ]

    m_gather_existing_template_names.assert_has_calls(gather_calls)

    assert P4TLG.template_cbox.count() == 2


def test_P4TemplateLoaderDialog_add_ui_elements_to_layout(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    P4TLG = P4TemplateLoaderDialog()
    assert isinstance(P4TLG.main_layout, QVBoxLayout)


def test_P4TemplateLoaderDialog_set_window_settings(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    P4TemplateLoaderDialog()


def test_P4TemplateLoaderDialog_connect_ui(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    P4TLG = P4TemplateLoaderDialog()


def test_P4TemplateLoaderDialog_edit_current_template(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    m_reload_ui = mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')
    m_P4TemplateEditorDialog = mocker.patch('p4templates.ui.p4_template_loader_gui.P4TemplateEditorDialog')

    P4TLG = P4TemplateLoaderDialog()

    P4TLG.template_path = 'template_path'
    reload_calls = [
        mocker.call(),
        mocker.call(),
    ]

    P4TLG.edit_current_template()

    m_reload_ui.assert_has_calls(reload_calls)

    m_P4TemplateEditorDialog.assert_called_once_with(template_path='template_path')


def test_P4TemplateLoaderDialog_edit_new_template(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    m_reload_ui = mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')
    m_P4TemplateEditorDialog = mocker.patch('p4templates.ui.p4_template_loader_gui.P4TemplateEditorDialog')

    P4TLG = P4TemplateLoaderDialog()

    reload_calls = [
        mocker.call(),
        mocker.call(),
    ]

    P4TLG.edit_new_template()

    m_reload_ui.assert_has_calls(reload_calls)

    m_P4TemplateEditorDialog.assert_called_once()


def test_P4TemplateLoaderDialog_process(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'reload_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_substitute_parameters = mocker.patch('p4templates.ui.p4_template_loader_gui.substitute_parameters', return_value='substituted_template_data')
    m_setup_server_connection = mocker.patch('p4templates.ui.p4_template_loader_gui.setup_server_connection', return_value='p4_connection')
    m_load_server_config = mocker.patch('p4templates.ui.p4_template_loader_gui.load_server_config', return_value={'server': {'key':'value'}})
    m_process_template = mocker.patch('p4templates.ui.p4_template_loader_gui.process_template')

    P4TLG = P4TemplateLoaderDialog()

    P4TLG.template_data = 'template_data'
    P4TLG.gathered_parameters = 'gathered_parameters'
    P4TLG.config_path = 'config_path'

    P4TLG.process()

    m_substitute_parameters.assert_called_once_with('template_data', 'gathered_parameters')
    m_setup_server_connection.assert_called_once_with(key='value')
    m_load_server_config.assert_called_once_with('config_path')
    m_process_template.assert_called_once_with('substituted_template_data', 'p4_connection')


def test_P4TemplateLoaderDialog_reload_ui(mocker):
    mocker.patch.object(P4TemplateLoaderDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateLoaderDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateLoaderDialog, 'connect_ui')
    mocker.patch.object(P4TemplateLoaderDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateLoaderDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_loader_gui.QDialog')

    m_update_template_combobox = mocker.patch.object(P4TemplateLoaderDialog, 'update_template_combobox')
    m_update_parameters_table = mocker.patch.object(P4TemplateLoaderDialog, 'update_parameters_table')

    P4TLG = P4TemplateLoaderDialog()

    m_update_template_combobox.assert_called_once()
    m_update_parameters_table.assert_called_once()