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

from __future__ import print_function

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QComboBox,
    QTableWidgetItem,
    QHeaderView,
)
from p4templates.ui.p4_template_editor_gui import P4TemplateEditorDialog
from p4templates.kernel.utils import (
    gather_existing_template_names,
    gather_parameters,
    read_json,
    substitute_parameters,
    convert_to_string,
    load_server_config,
    setup_server_connection,
)
from p4templates.kernel.process_template import process_template


class P4TemplateLoaderDialog(QDialog):
    def __init__(self, parent=None, config_path=None, template_dir=None):
        super(P4TemplateLoaderDialog, self).__init__(parent)
        self.gathered_parameters = {}
        self.template_dir = template_dir or ''
        self.template_path = ''
        self.template_data = ""
        self.config_path = config_path or ''
        self.existing_template_lut = {}

        # UI Setup
        self.create_ui_elements()
        self.add_ui_elements_to_layout()
        self.connect_ui()
        self.set_window_settings()

        # Data Setup
        self.reload_ui()

        self.exec()

    def create_ui_elements(self):
        self.template_cbox = QComboBox()

        self.btn_new = QPushButton("New")
        self.btn_edit = QPushButton("Edit")
        self.btn_run = QPushButton("Run")

        self.parameter_table = QTableWidget()
        self.parameter_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.parameter_table.horizontalHeader().setVisible(False)
        self.parameter_table.verticalHeader().setVisible(False)
        self.parameter_table.setColumnCount(2)

    def update_parameters(self):
        self.gathered_parameters = {}
        for row in range(self.parameter_table.rowCount()):
            if self.parameter_table.item(row, 0) and self.parameter_table.item(row, 1):
                parameter = self.parameter_table.item(row, 0).text()
                value = self.parameter_table.item(row, 1).text()
                self.gathered_parameters[parameter] = value


        self.validate_parameters()

    def validate_parameters(self):
        valid = True
        for _, value in self.gathered_parameters.items():
            if not value or " " in value:
                valid = False
                break

        if valid:
            self.btn_run.setEnabled(True)
        else:
            self.btn_run.setEnabled(False)

    def update_parameters_table(self):
        while self.parameter_table.rowCount():
            self.parameter_table.removeRow(0)

        if not self.template_cbox.currentText():
            return

        self.template_path = self.existing_template_lut[
            self.template_cbox.currentText()
        ]
        self.template_data = read_json(self.template_path)
        self.gathered_parameters = {
            _: "" for _ in gather_parameters(self.template_data)
        }

        self.parameter_table.setRowCount(len(self.gathered_parameters))
        for i, key in enumerate(self.gathered_parameters):
            key_item = QTableWidgetItem(key)
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.parameter_table.setItem(i, 0, key_item)
            self.parameter_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(self.gathered_parameters.get(key, ""))
                ),
            )

        self.validate_parameters()

    def update_template_combobox(self):
        self.template_cbox.clear()
        self.existing_template_lut = gather_existing_template_names(self.template_dir)
        for template_name in self.existing_template_lut:
            self.template_cbox.addItem(template_name)

    def add_ui_elements_to_layout(self):
        self.main_layout = QVBoxLayout()

        self.main_btn_row = QHBoxLayout()
        self.main_btn_row.addWidget(self.btn_new)
        self.main_btn_row.addWidget(self.btn_edit)
        self.main_btn_row.addWidget(self.btn_run)

        self.main_layout.addWidget(self.template_cbox)
        self.main_layout.addWidget(self.parameter_table)
        self.main_layout.addLayout(self.main_btn_row)

        self.setLayout(self.main_layout)

    def set_window_settings(self):
        self.setWindowTitle("P4 Project Templates")
        self.setMinimumSize(200, 300)

    def connect_ui(self):
        self.btn_edit.clicked.connect(self.edit_current_template)
        self.btn_new.clicked.connect(self.edit_new_template)
        self.template_cbox.currentTextChanged.connect(self.update_parameters_table)
        self.parameter_table.cellChanged.connect(self.update_parameters)
        self.btn_run.clicked.connect(self.process)

    def edit_current_template(self):
        editor_gui = P4TemplateEditorDialog(template_path=self.template_path)
        self.reload_ui()

    def edit_new_template(self):
        editor_gui = P4TemplateEditorDialog()
        self.reload_ui()

    def process(self):
        template_data = substitute_parameters(
            self.template_data, self.gathered_parameters
        )
        print("Connecting to server:")
        p4_connection = setup_server_connection(**load_server_config(self.config_path)['server'])
        print(p4_connection, "\n")

        print("Processing template:")
        process_template(template_data, p4_connection)
        print("Finished!")

    def reload_ui(self):
        self.update_template_combobox()
        self.update_parameters_table()
