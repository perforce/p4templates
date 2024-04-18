import pytest
from p4templates.ui.p4_template_editor_gui import (
    GetTypeNameDialog, 
    P4TemplateEditorDialog, 
    QHeaderView, 
    QDialog,
    QTableWidgetItem,
    Qt,
    convert_to_string
)




class MockQDialog(QDialog):
    def __init__(self, parent=None, ):
        super(MockQDialog, self).__init__(parent)

    def setLayout(self):
        pass


class MockGetTypeNameDialog(object):
     def __init__(self, type_name):
          self.type_name = type_name


def test_GetTypeNameDialog_init(qtbot,mocker):
    m_exec = mocker.patch.object(GetTypeNameDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    GTND = GetTypeNameDialog()
    qtbot.addWidget(GTND)

    assert isinstance(GTND, GetTypeNameDialog)

    m_exec.assert_called_once()


def test_GetTypeNameDialog_cancel_clicked(qtbot,mocker):
    mocker.patch.object(GetTypeNameDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
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
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
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
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

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
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    m_QPushButton = mocker.patch('p4templates.ui.p4_template_editor_gui.QPushButton')
    m_QTabWidget = mocker.patch('p4templates.ui.p4_template_editor_gui.QTabWidget')
    m_QWidget = mocker.patch('p4templates.ui.p4_template_editor_gui.QWidget')
    m_QListWidget = mocker.patch('p4templates.ui.p4_template_editor_gui.QListWidget')
    m_QTableWidget = mocker.patch('p4templates.ui.p4_template_editor_gui.QTableWidget')

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
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    assert isinstance(P4TEG, P4TemplateEditorDialog)


def test_P4TemplateEditorDialog_set_window_settings(mocker, qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)


def test_P4TemplateEditorDialog_connect_ui(mocker, qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)


def test_P4TemplateEditorDialog_populate_data(mocker, qtbot):
    # mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    m_populate_depot_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_depot_data')
    m_populate_group_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_group_data')
    m_populate_user_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_user_data')
    m_populate_stream_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_stream_data')
    m_populate_protection_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_protection_data')
    m_populate_typemap_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_typemap_data')
    m_populate_branch_data = mocker.patch.object(P4TemplateEditorDialog, 'populate_branch_data')

    m_os_path_isfile = mocker.patch('p4templates.ui.p4_template_editor_gui.os.path.isfile', return_value=True)
    m_read_json = mocker.patch('p4templates.ui.p4_template_editor_gui.read_json', return_value={})

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
    mocker.patch.object(P4TemplateEditorDialog, 'create_ui_elements')
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    m_QFileDialog = mocker.patch('p4templates.ui.p4_template_editor_gui.QFileDialog.getSaveFileName', return_value=('file_name', 'mock'))
    m_write_json = mocker.patch('p4templates.ui.p4_template_editor_gui.write_json')


    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_path = '/a/fake/template/path'
    P4TEG.template_data = {'key':'value'}

    P4TEG.save_data()

    m_QFileDialog.assert_called_once_with(P4TEG, 'Save File', '/a/fake/template/path', 'Text Files(*.json)')
    m_write_json.assert_called_once_with({'key':'value'}, m_QFileDialog.return_value[0])


def test_P4TemplateEditorDialog_populate_depot_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'depots': [{'name': 'test'}]}
    
    P4TEG.populate_depot_data()
    
    assert P4TEG.depot_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'depots': [{'name': 'test'}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_depot_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    P4TEG.populate_depot_data()

    P4TEG.reload_selected_depot_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_depot(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_depot_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_depot_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_depot()
    P4TEG.add_new_depot()
    P4TEG.add_new_depot()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'depots':[
            {'name': 'NewDepot'}, 
            {'name': 'NewDepot1'},
            {'name': 'NewDepot2'},

        ]
    }
    
    m_populate_depot_data.assert_has_calls(pop_calls)
    

def test_P4TemplateEditorDialog_remove_depot(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_depot_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_depot_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_depot()

    P4TEG.template_data = {
        'depots':[
            {'name': 'NewDepot'}, 
            {'name': 'NewDepot1'}, 
        ]
    }
    P4TEG.depot_list.addItem('NewDepot')
    P4TEG.depot_list.addItem('NewDepot1')

    P4TEG.depot_list.setCurrentRow(0)
    P4TEG.depot_list.setCurrentItem(P4TEG.depot_list.item(0))
    
    P4TEG.remove_depot()

    assert P4TEG.template_data == {
        'depots':[
            {'name': 'NewDepot1'}, 
        ]
    }
    
    m_populate_depot_data.assert_called_once()

    
def test_P4TemplateEditorDialog_update_current_depot_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_depot_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {
        'depots':[
            {'name': 'NewDepot'}, 
        ]
    }

    for depot in P4TEG.template_data.get('depots', []):
        P4TEG.depot_list.addItem(depot.get('name', ''))

    P4TEG.depot_list.setCurrentRow(0)
    P4TEG.depot_list.setCurrentItem(P4TEG.depot_list.item(0))

    for i, key in enumerate(["name", "type", "depth", "user"]):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.depot_table.setItem(i, 0, key_item)
            P4TEG.depot_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["depots"][0].get(
                            key, P4TEG.defaults["depot"][key]
                        )
                    )
                ),
            )

    P4TEG.template_data = {'depots':[]}

    P4TEG.update_current_depot_data() # no current depot

    P4TEG.template_data = {'depots':[{'name': 'NewDepot'}, ]}

    P4TEG.update_current_depot_data() # real deal

    assert P4TEG.template_data == {'depots': [{'depth': '1', 'name': 'NewDepot', 'type': 'stream', 'user': ''}]}


def test_P4TemplateEditorDialog_populate_group_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'groups': [{'name': 'test'}]}
    
    P4TEG.populate_group_data()
    
    assert P4TEG.group_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'groups': [{'name': 'test'}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_group_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    P4TEG.populate_group_data()

    P4TEG.reload_selected_group_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_group(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_group_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_group_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_group()
    P4TEG.add_new_group()
    P4TEG.add_new_group()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'groups':[
            {'name': 'NewGroup'}, 
            {'name': 'NewGroup1'},
            {'name': 'NewGroup2'},
        ]
    }
    
    m_populate_group_data.assert_has_calls(pop_calls)


def test_P4TemplateEditorDialog_remove_group(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_group_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_group_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_group()

    P4TEG.template_data = {
        'groups':[
            {'name': 'NewGroup'}, 
            {'name': 'NewGroup1'}, 
        ]
    }
    P4TEG.group_list.addItem('NewGroup')
    P4TEG.group_list.addItem('NewGroup1')

    P4TEG.group_list.setCurrentRow(0)
    P4TEG.group_list.setCurrentItem(P4TEG.group_list.item(0))
    
    P4TEG.remove_group()

    assert P4TEG.template_data == {
        'groups':[
            {'name': 'NewGroup1'}, 
        ]
    }
    
    m_populate_group_data.assert_called_once()


def test_P4TemplateEditorDialog_update_current_group_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_group_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'groups':[{'name': 'NewGroup'}]}

    for group in P4TEG.template_data.get('groups', []):
        P4TEG.group_list.addItem(group.get('name', ''))

    P4TEG.group_list.setCurrentRow(0)
    P4TEG.group_list.setCurrentItem(P4TEG.group_list.item(0))

    for i, key in enumerate(P4TEG.defaults["group"].keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.group_table.setItem(i, 0, key_item)
            P4TEG.group_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["groups"][0].get(
                            key, P4TEG.defaults["group"][key]
                        )
                    )
                ),
            )

    P4TEG.template_data = {'groups':[]}

    P4TEG.update_current_group_data() # no current depot

    P4TEG.template_data = {'groups':[{'name': 'NewGroup'}]}

    P4TEG.update_current_group_data() # real deal
    
    assert P4TEG.template_data == {'groups': [{'name': 'NewGroup', 'description': '', 'max_results': 'unset', 'max_scan_rows': 'unset', 'max_lock_time': 'unset', 'max_open_files': 'unset', 'timeout': '43200', 'password_timeout': 'unset', 'subgroups': '', 'owners': '', 'users': ''}]}


def test_P4TemplateEditorDialog_populate_user_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'users': [{'name': 'test'}]}
    
    P4TEG.populate_user_data()
    
    assert P4TEG.user_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'users': [{'name': 'test'}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_user_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    P4TEG.populate_user_data()

    P4TEG.reload_selected_user_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_user(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_user_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_user_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_user()
    P4TEG.add_new_user()
    P4TEG.add_new_user()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'users':[
            {'name': 'NewUser'}, 
            {'name': 'NewUser1'},
            {'name': 'NewUser2'},
        ]
    }
    
    m_populate_user_data.assert_has_calls(pop_calls)


def test_P4TemplateEditorDialog_remove_user(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_user_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_user_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_user()

    P4TEG.template_data = {
        'users':[
            {'name': 'NewUser'}, 
            {'name': 'NewUser1'}, 
        ]
    }
    P4TEG.user_list.addItem('NewUser')
    P4TEG.user_list.addItem('NewUser1')

    P4TEG.user_list.setCurrentRow(0)
    P4TEG.user_list.setCurrentItem(P4TEG.user_list.item(0))
    
    P4TEG.remove_user()

    assert P4TEG.template_data == {
        'users':[
            {'name': 'NewUser1'}, 
        ]
    }
    
    m_populate_user_data.assert_called_once()


def test_P4TemplateEditorDialog_update_current_user_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_user_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'users':[{'name': 'NewUser'}]}

    for user in P4TEG.template_data.get('users', []):
        P4TEG.user_list.addItem(user.get('name', ''))

    P4TEG.user_list.setCurrentRow(0)
    P4TEG.user_list.setCurrentItem(P4TEG.user_list.item(0))

    for i, key in enumerate(P4TEG.defaults["user"].keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.user_table.setItem(i, 0, key_item)
            P4TEG.user_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["users"][0].get(
                            key, P4TEG.defaults["user"][key]
                        )
                    )
                ),
            )

    P4TEG.template_data = {'users':[]}

    P4TEG.update_current_user_data() # no current depot

    P4TEG.template_data = {'users':[{'name': 'NewUser'}]}

    P4TEG.update_current_user_data() # real deal
    print(P4TEG.template_data)
    assert P4TEG.template_data == {'users': [{'name': 'NewUser', 'email': '', 'full_name': '', 'auth_method': '', 'reviews': '', 'job_view': ''}]}


def test_P4TemplateEditorDialog_populate_stream_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'streams': [{'name': 'test'}]}
    
    P4TEG.populate_stream_data()
    
    assert P4TEG.stream_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'streams': [{'name': 'test', 'paths': ['share ...'], 'remapped':['rempapped'], 'ignored': ['ignore']}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_stream_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    P4TEG.populate_stream_data()

    P4TEG.reload_selected_stream_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_stream(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_stream_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_stream_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_stream()
    P4TEG.add_new_stream()
    P4TEG.add_new_stream()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'streams':[
            {'name': 'NewStream'}, 
            {'name': 'NewStream1'},
            {'name': 'NewStream2'},
        ]
    }
    
    m_populate_stream_data.assert_has_calls(pop_calls)


def test_P4TemplateEditorDialog_remove_stream(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_stream_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_stream_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_stream()

    P4TEG.template_data = {
        'streams':[
            {'name': 'NewStream'}, 
            {'name': 'NewStream1'}, 
        ]
    }
    P4TEG.stream_list.addItem('NewStream')
    P4TEG.stream_list.addItem('NewStream1')

    P4TEG.stream_list.setCurrentRow(0)
    P4TEG.stream_list.setCurrentItem(P4TEG.stream_list.item(0))
    
    P4TEG.remove_stream()

    assert P4TEG.template_data == {
        'streams':[
            {'name': 'NewStream1'}, 
        ]
    }
    
    m_populate_stream_data.assert_called_once()


def test_P4TemplateEditorDialog_update_current_stream_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_stream_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'streams':[{'name': 'NewStream'}]}

    for stream in P4TEG.template_data.get('streams', []):
        P4TEG.stream_list.addItem(stream.get('name', ''))

    P4TEG.stream_list.setCurrentRow(0)
    P4TEG.stream_list.setCurrentItem(P4TEG.stream_list.item(0))

    for i, key in enumerate(P4TEG.defaults["stream"].keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.stream_table.setItem(i, 0, key_item)
            P4TEG.stream_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["streams"][0].get(
                            key, P4TEG.defaults["stream"][key]
                        )
                    )
                ),
            )

    P4TEG.template_data = {'streams':[]}

    P4TEG.update_current_stream_data() # no current depot

    P4TEG.template_data = {'streams':[{'name': 'NewStream'}]}

    P4TEG.update_current_stream_data() # real deal
    print(P4TEG.template_data)
    assert P4TEG.template_data == {'streams': [{'name': 'NewStream', 'type': 'mainline', 'depot': '', 'user': 'None', 'view': 'inherit', 'parent': '', 'options': 'allsubmit unlocked notoparent nofromparent mergedown'}]}


def test_P4TemplateEditorDialog_update_current_stream_path_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_stream_path_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'streams':[{'name': 'NewStream'}]}

    for stream in P4TEG.template_data.get('streams', []):
        P4TEG.stream_list.addItem(stream.get('name', ''))

    P4TEG.stream_list.setCurrentRow(0)
    P4TEG.stream_list.setCurrentItem(P4TEG.stream_list.item(0))

    P4TEG.template_data = {'streams':[]}

    P4TEG.update_current_stream_path_data() # no current depot

    P4TEG.stream_paths_table.setRowCount(3)
    for i, value in enumerate(['path1', 'path2']):
            value_item = QTableWidgetItem(value)
            P4TEG.stream_paths_table.setItem(i, 0, value_item)
    

    P4TEG.template_data = {'streams':[{'name': 'NewStream', 'paths': ['path1', 'path2']}]}

    P4TEG.update_current_stream_path_data() # real deal

    assert P4TEG.stream_paths_table.rowCount() == 3


def test_P4TemplateEditorDialog_update_current_stream_remapped_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_stream_remapped_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'streams':[{'name': 'NewStream'}]}

    for stream in P4TEG.template_data.get('streams', []):
        P4TEG.stream_list.addItem(stream.get('name', ''))

    P4TEG.stream_list.setCurrentRow(0)
    P4TEG.stream_list.setCurrentItem(P4TEG.stream_list.item(0))

    P4TEG.template_data = {'streams':[]}

    P4TEG.update_current_stream_remapped_data() # no current depot

    P4TEG.stream_remapped_table.setRowCount(3)
    for i, value in enumerate(['path1', 'path2']):
            value_item = QTableWidgetItem(value)
            P4TEG.stream_remapped_table.setItem(i, 0, value_item)
    

    P4TEG.template_data = {'streams':[{'name': 'NewStream', 'remapped': ['path1', 'path2']}]}

    P4TEG.update_current_stream_remapped_data() # real deal

    assert P4TEG.stream_remapped_table.rowCount() == 3


def test_P4TemplateEditorDialog_update_current_stream_ignored_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_stream_ignored_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'streams':[{'name': 'NewStream'}]}

    for stream in P4TEG.template_data.get('streams', []):
        P4TEG.stream_list.addItem(stream.get('name', ''))

    P4TEG.stream_list.setCurrentRow(0)
    P4TEG.stream_list.setCurrentItem(P4TEG.stream_list.item(0))

    P4TEG.template_data = {'streams':[]}

    P4TEG.update_current_stream_ignored_data() # no current depot

    P4TEG.stream_ignored_table.setRowCount(3)
    for i, value in enumerate(['path1', 'path2']):
            value_item = QTableWidgetItem(value)
            P4TEG.stream_ignored_table.setItem(i, 0, value_item)
    

    P4TEG.template_data = {'streams':[{'name': 'NewStream', 'ignored': ['path1', 'path2']}]}

    P4TEG.update_current_stream_ignored_data() # real deal

    assert P4TEG.stream_ignored_table.rowCount() == 3


def test_P4TemplateEditorDialog_populate_protection_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'protections': [{'name': 'test'}]}
    
    P4TEG.populate_protection_data()
    
    assert P4TEG.protection_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'protections': [{'name': 'test'}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_protection_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    P4TEG.populate_protection_data()

    P4TEG.reload_selected_protection_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_protection(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_protection_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_protection_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_protection()
    P4TEG.add_new_protection()
    P4TEG.add_new_protection()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'protections':[
            {'name': 'NewProtection'}, 
            {'name': 'NewProtection1'},
            {'name': 'NewProtection2'},

        ]
    }
    
    m_populate_protection_data.assert_has_calls(pop_calls)
    

def test_P4TemplateEditorDialog_remove_protection(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_protection_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_protection_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_protection()

    P4TEG.template_data = {
        'protections':[
            {'name': 'NewProtection'}, 
            {'name': 'NewProtection1'}, 
        ]
    }
    P4TEG.protection_list.addItem('NewProtection')
    P4TEG.protection_list.addItem('NewProtection1')

    P4TEG.protection_list.setCurrentRow(0)
    P4TEG.protection_list.setCurrentItem(P4TEG.protection_list.item(0))
    
    P4TEG.remove_protection()

    assert P4TEG.template_data == {
        'protections':[
            {'name': 'NewProtection1'}, 
        ]
    }
    
    m_populate_protection_data.assert_called_once()

    
def test_P4TemplateEditorDialog_update_current_protection_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_protection_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {
        'protections':[
            {'name': 'NewProtection'}, 
        ]
    }

    for prot in P4TEG.template_data.get('protections', []):
        P4TEG.protection_list.addItem(prot.get('name', ''))

    P4TEG.protection_list.setCurrentRow(0)
    P4TEG.protection_list.setCurrentItem(P4TEG.protection_list.item(0))

    for i, key in enumerate(P4TEG.defaults["protection"].keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.protection_table.setItem(i, 0, key_item)
            P4TEG.protection_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["protections"][0].get(
                            key, P4TEG.defaults["protection"][key]
                        )
                    )
                ),
            )

    P4TEG.template_data = {'protections':[]}

    P4TEG.update_current_protection_data() # no current depot

    P4TEG.template_data = {'protections':[{'name': 'NewProtection'}, ]}

    P4TEG.update_current_protection_data() # real deal

    assert P4TEG.template_data == {'protections': [{'name': 'NewProtection', 'access': '', 'type': '', 'host': '*', 'path': '', 'comment': ''}]}


def test_P4TemplateEditorDialog_populate_typemap_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'types': {'type': ['test']}}
    
    P4TEG.populate_typemap_data()
    
    assert P4TEG.typemap_type_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data,type_name,expected_results',
        [
            ({}, 'type', {'types': {'type': []}}),
            ({}, '', {}),
            ({'types': {'type': [],'type1': []}}, 'type', {'types': {'type': [], 'type1': [], 'type2': []}}),
        ]
)
def test_P4TemplateEditorDialog_add_typemap_type(mocker,qtbot, template_data, type_name, expected_results):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_typemap_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_typemap_data')
    m_GetTypeNameDialog = mocker.patch('p4templates.ui.p4_template_editor_gui.GetTypeNameDialog', return_value=MockGetTypeNameDialog(type_name)) 

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = template_data

    P4TEG.add_typemap_type()
    print(P4TEG.template_data)
    assert P4TEG.template_data == expected_results
    
    if type_name:
        m_populate_typemap_data.assert_called_once()
    else:
         m_populate_typemap_data.assert_not_called()

    m_GetTypeNameDialog.assert_called_once()


def test_P4TemplateEditorDialog_remove_typemap_type(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_typemap_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_typemap_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_typemap_type()

    P4TEG.template_data = {
        'types': {
             'type':  [],
             'type1':  [],
        }, 

    }
    P4TEG.typemap_type_list.addItem('type')
    P4TEG.typemap_type_list.addItem('type1')

    P4TEG.typemap_type_list.setCurrentRow(0)
    P4TEG.typemap_type_list.setCurrentItem(P4TEG.typemap_type_list.item(0))
    
    P4TEG.remove_typemap_type()

    assert P4TEG.template_data == {
        'types': {
             'type1':  [],
        }, 

    }
    
    m_populate_typemap_data.assert_called_once()


@pytest.mark.parametrize(
        'template_data,type_name,expected_results',
        [
            ({'types': {'type': []}}, 'type1', {'types': {'type1': []}}),
            ({'types': {'type': []}}, '', {'types': {'type': []}}),
            ({}, '', {}),
        ]
)
def test_P4TemplateEditorDialog_edit_typemap_type(mocker,qtbot, template_data, type_name, expected_results):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_typemap_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_typemap_data')
    m_GetTypeNameDialog = mocker.patch('p4templates.ui.p4_template_editor_gui.GetTypeNameDialog', return_value=MockGetTypeNameDialog(type_name)) 

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    

    for type in P4TEG.template_data.get('types', []):
        P4TEG.typemap_type_list.addItem(type)

    if template_data:
        P4TEG.typemap_type_list.setCurrentRow(0)
        P4TEG.typemap_type_list.setCurrentItem(P4TEG.typemap_type_list.item(0))

    P4TEG.edit_typemap_type()

    print(P4TEG.template_data)
    assert P4TEG.template_data == expected_results
    
    if template_data:
        m_GetTypeNameDialog.assert_called_once()
    else:
        m_GetTypeNameDialog.assert_not_called()
    if type_name:
        m_populate_typemap_data.assert_called_once()
        
    else:
         m_populate_typemap_data.assert_not_called()
         

@pytest.mark.parametrize(
        'template_data',
        [
            ({'types': {'type': ['path1', 'path2']}}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_typemap_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    for type in P4TEG.template_data.get('types', {}).keys():
        P4TEG.typemap_type_list.addItem(type)

    if P4TEG.template_data.get('types', {}):
        P4TEG.typemap_type_list.setCurrentRow(0)
        P4TEG.typemap_type_list.setCurrentItem(P4TEG.typemap_type_list.item(0))

    P4TEG.populate_typemap_data()

    P4TEG.reload_selected_typemap_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_update_current_typemap_path_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_typemap_path_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'types':{'type': ['path']}}

    for type in P4TEG.template_data.get('types', {}).keys():
        P4TEG.typemap_type_list.addItem(type)

    P4TEG.typemap_type_list.setCurrentRow(0)
    P4TEG.typemap_type_list.setCurrentItem(P4TEG.typemap_type_list.item(0))

    P4TEG.template_data = {'types':{}}
    P4TEG.update_current_typemap_path_data() # no current depot
    
    P4TEG.typemap_path_table.setRowCount(3)
    for i, value in enumerate(['path1', 'path2']):
            value_item = QTableWidgetItem(value)
            value_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.typemap_path_table.setItem(i, 0, value_item)
    
    P4TEG.update_current_typemap_path_data() # real deal
    print(P4TEG.template_data)
    assert P4TEG.template_data == {'types': {'type': ['path1', 'path2']}}


def test_P4TemplateEditorDialog_populate_branch_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.template_data = {'branches': [{'name': 'test'}]}
    
    P4TEG.populate_branch_data()
    
    assert P4TEG.branch_list.count() == 1
    assert P4TEG.item_load == False


@pytest.mark.parametrize(
        'template_data',
        [
            ({'branches': [{'name': 'test', 'view': {'old_path': 'new_path'}}]}),
            ({}),
        ]
)
def test_P4TemplateEditorDialog_reload_selected_branch_data(mocker,qtbot, template_data):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)
    
    P4TEG.template_data = template_data
    
    for branch in P4TEG.template_data.get('branches', []):
        P4TEG.branch_list.addItem(branch['name'])

    if P4TEG.template_data.get('branches', []):
        P4TEG.branch_list.setCurrentRow(0)
        P4TEG.branch_list.setCurrentItem(P4TEG.branch_list.item(0))

    P4TEG.populate_branch_data()

    P4TEG.reload_selected_branch_data()

    assert P4TEG.item_load == False


def test_P4TemplateEditorDialog_add_new_branch(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_branch_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_branch_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.add_new_branch()
    P4TEG.add_new_branch()
    P4TEG.add_new_branch()

    pop_calls = [
        mocker.call(),
        mocker.call(),
        mocker.call(),
    ]

    assert P4TEG.template_data == {
        'branches':[
            {'name': 'NewBranch'}, 
            {'name': 'NewBranch1'},
            {'name': 'NewBranch2'},

        ]
    }
    
    m_populate_branch_data.assert_has_calls(pop_calls)
   

def test_P4TemplateEditorDialog_remove_branch(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')
    
    m_populate_branch_data =  mocker.patch.object(P4TemplateEditorDialog, 'populate_branch_data')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.remove_branch()

    P4TEG.template_data = {
        'branches':[
            {'name': 'NewBranch'}, 
            {'name': 'NewBranch1'}, 
        ]
    }

    P4TEG.branch_list.addItem('NewBranch')
    P4TEG.branch_list.addItem('NewBranch1')

    P4TEG.branch_list.setCurrentRow(0)
    P4TEG.branch_list.setCurrentItem(P4TEG.branch_list.item(0))
    
    P4TEG.remove_branch()

    assert P4TEG.template_data == {
        'branches':[
            {'name': 'NewBranch1'}, 
        ]
    }
    
    m_populate_branch_data.assert_called_once()


def test_P4TemplateEditorDialog_update_current_branch_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_branch_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'branches':[{'name': 'NewBranch'}]}

    for branch in P4TEG.template_data.get('branches', []):
        P4TEG.branch_list.addItem(branch['name'])

    P4TEG.branch_list.setCurrentRow(0)
    P4TEG.branch_list.setCurrentItem(P4TEG.branch_list.item(0))

    P4TEG.template_data = {'branches':[]}
    P4TEG.update_current_branch_data() # no current depot
    
    P4TEG.template_data = {'branches':[{'name': 'NewBranch'}]}

    P4TEG.branch_table.setRowCount(3)
    for i, key in enumerate(P4TEG.defaults['branch'].keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.branch_table.setItem(i, 0, key_item)
            P4TEG.branch_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        P4TEG.template_data["branches"][0].get(
                            key, P4TEG.defaults["branch"][key]
                        )
                    )
                ),
            )
    
    P4TEG.update_current_branch_data() # real deal

    assert P4TEG.template_data == {'branches': [{'name': 'NewBranch', 'owner': '', 'options': ['unlocked']}]}

def test_P4TemplateEditorDialog_update_current_branch_view_data(mocker,qtbot):
    mocker.patch.object(P4TemplateEditorDialog, 'add_ui_elements_to_layout')
    mocker.patch.object(P4TemplateEditorDialog, 'connect_ui')
    mocker.patch.object(P4TemplateEditorDialog, 'set_window_settings')
    mocker.patch.object(P4TemplateEditorDialog, 'populate_data')
    mocker.patch.object(P4TemplateEditorDialog, 'exec')
    mocker.patch('p4templates.ui.p4_template_editor_gui.QDialog')

    P4TEG = P4TemplateEditorDialog()
    qtbot.addWidget(P4TEG)

    P4TEG.item_load = True
    P4TEG.update_current_branch_view_data() # item load
    P4TEG.item_load = False

    P4TEG.template_data = {'branches':[{'name': 'NewBranch'}]}

    for branch in P4TEG.template_data.get('branches', []):
        P4TEG.branch_list.addItem(branch['name'])

    P4TEG.branch_list.setCurrentRow(0)
    P4TEG.branch_list.setCurrentItem(P4TEG.branch_list.item(0))

    P4TEG.template_data = {'branches':[]}
    P4TEG.update_current_branch_view_data() # no current depot
    
    P4TEG.template_data = {'branches':[{'name': 'NewBranch'}]}
    mock_view_data = {'old_path1': 'new_path1', 'old_path2': 'new_path2'}
    P4TEG.branch_view_table.setRowCount(3)
    for i, key in enumerate(mock_view_data.keys()):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            P4TEG.branch_view_table.setItem(i, 0, key_item)
            P4TEG.branch_view_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    mock_view_data[key]
                )
            ),
    
    P4TEG.update_current_branch_view_data() # real deal
    
    assert P4TEG.template_data ==  {'branches': [{'name': 'NewBranch', 'view': {'Old_path1': 'new_path1', 'Old_path2': 'new_path2'}}]}
