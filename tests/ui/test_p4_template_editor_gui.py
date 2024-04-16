import pytest
from p4_templates.ui.p4_template_editor_gui import (
    GetTypeNameDialog, 
    P4TemplateEditorDialog, 
    QHeaderView, 
    QDialog,    
    QVBoxLayout,
    QHBoxLayout,
)


class MockQDialog(QDialog):
    def __init__(self, parent=None, ):
        super(MockQDialog, self).__init__(parent)

    def setLayout(self):
        pass


def test_GetTypeNameDialog_init(qtbot,mocker):
    m_exec = mocker.patch.object(GetTypeNameDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    GTND = GetTypeNameDialog()
    qtbot.addWidget(GTND)

    assert isinstance(GTND, GetTypeNameDialog)

    m_exec.assert_called_once()


def test_GetTypeNameDialog_cancel_clicked(qtbot,mocker):
    mocker.patch.object(GetTypeNameDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')
    m_close = mocker.patch.object(GetTypeNameDialog, 'close')

    GTND = GetTypeNameDialog()
    qtbot.addWidget(GTND)

    GTND.type_name = "something_else"
    assert GTND.type_name == "something_else"

    GTND.cancel_clicked()

    assert GTND.type_name == None
    m_close.assert_called_once()


def test_GetTypeNameDialog_ok_clicked(qtbot,mocker):
    mocker.patch.object(GetTypeNameDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')
    m_close = mocker.patch.object(GetTypeNameDialog, 'close')

    GTND = GetTypeNameDialog()
    qtbot.addWidget(GTND)

    GTND.type_textedit.setText('something_else')

    GTND.type_name = "something"
    assert GTND.type_name == "something"

    GTND.ok_clicked()

    assert GTND.type_name == 'something_else'
    m_close.assert_called_once()


def test_P4TemplateEditorDialog_init(mocker,qtbot):
    m_create_ui_elements = mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    m_add_ui_elements_to_layout = mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    m_connect_ui = mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    m_set_window_settings = mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    m_populate_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    m_exec = mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    assert isinstance(P4TEG, P4TemplateEditorDialog)
    m_create_ui_elements.assert_called_once()
    m_add_ui_elements_to_layout.assert_called_once()
    m_connect_ui.assert_called_once()
    m_set_window_settings.assert_called_once()
    m_populate_data.assert_called_once()
    m_exec.assert_called_once()


def test_P4TemplateEditorDialog_create_ui_elements(mocker, qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    m_QPushButton = mocker.patch('p4_templates.ui.p4_template_editor_gui.QPushButton')
    m_QTabWidget = mocker.patch('p4_templates.ui.p4_template_editor_gui.QTabWidget')
    m_QWidget = mocker.patch('p4_templates.ui.p4_template_editor_gui.QWidget')
    m_QListWidget = mocker.patch('p4_templates.ui.p4_template_editor_gui.QListWidget')
    m_QTableWidget = mocker.patch('p4_templates.ui.p4_template_editor_gui.QTableWidget')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)


    P4TEG.create_ui_elements()


    push_calls = [
        mocker.call('Reload'),
        mocker.call('Save'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('…'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('Reload'),
        mocker.call('Save'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('…'),
        mocker.call('-'),
        mocker.call('+'),
        mocker.call('-'),
    ]
    
    tab_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]
    
    wid_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]
    
    list_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]
    
    table_calls = [
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(4),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(7),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(11),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(6),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(6),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(3),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(4),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(7),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(11),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(6),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(6),
        mocker.call(),
        mocker.call().setColumnCount(1),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2),
        mocker.call().setRowCount(3),
        mocker.call(),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch),
        mocker.call().horizontalHeader(),
        mocker.call().horizontalHeader().setVisible(False),
        mocker.call().verticalHeader(),
        mocker.call().verticalHeader().setVisible(False),
        mocker.call().setColumnCount(2)
]

    m_QPushButton.assert_has_calls(push_calls)
    m_QTabWidget.assert_has_calls(tab_calls)
    m_QWidget.assert_has_calls(wid_calls)
    m_QListWidget.assert_has_calls(list_calls)
    m_QTableWidget.assert_has_calls(table_calls)
 

def test_P4TemplateEditorDialog_add_ui_elements_to_layout(mocker, qtbot, monkeypatch):
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    assert isinstance(P4TEG, P4TemplateEditorDialog)


def test_P4TemplateEditorDialog_set_window_settings(mocker, qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

def test_P4TemplateEditorDialog_connect_ui(mocker, qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

def test_P4TemplateEditorDialog_populate_data(mocker, qtbot):
    # mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4_templates.ui.p4_template_editor_gui.QDialog')

    m_populate_depot_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_depot_data')
    m_populate_group_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_group_data')
    m_populate_user_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_user_data')
    m_populate_stream_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_stream_data')
    m_populate_protection_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_protection_data')
    m_populate_typemap_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_typemap_data')
    m_populate_branch_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_branch_data')

    m_os_path_isfile = mocker.patch('p4_templates.ui.p4_template_editor_gui.os.path.isfile', return_value=True)
    m_read_json = mocker.patch('p4_templates.ui.p4_template_editor_gui.read_json', return_value={})

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_path ='yep'

    P4TEG.populate_data()

    m_populate_depot_data.assert_called()
    m_populate_group_data.assert_called()
    m_populate_user_data.assert_called()
    m_populate_stream_data.assert_called()
    m_populate_protection_data.assert_called()
    m_populate_typemap_data.assert_called()
    m_populate_branch_data.assert_called()
    m_os_path_isfile.assert_called_once_with('yep')
    m_read_json.assert_called_with('yep')

def test_P4TemplateEditorDialog_save_data(mocker, qtbot):
    pass