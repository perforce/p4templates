import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QListWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
)

from p4_templates.kernel.utils import read_json, convert_to_string, write_json


class GetTypeNameDialog(QDialog):
    def __init__(self, parent=None, type_name="TypeName"):
        super(GetTypeNameDialog, self).__init__(parent)
        self.type_name = type_name
        self.type_textedit = QLineEdit(self.type_name)

        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")

        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.ok_btn.clicked.connect(self.ok_clicked)

        self.btn_layout.addWidget(self.cancel_btn)
        self.btn_layout.addWidget(self.ok_btn)
        self.main_layout.addWidget(self.type_textedit)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)

        self.exec()

    def cancel_clicked(self):
        self.type_name = None
        self.close()

    def ok_clicked(self):
        self.type_name = self.type_textedit.text()
        self.close()


class P4TemplateEditorDialog(QDialog):
    def __init__(self, parent=None, template_path=None):
        super(P4TemplateEditorDialog, self).__init__(parent)
        self.template_path = template_path
        self.item_load = False
        self.defaults = {
            "depot": {
                "name": "",
                "type": "stream",
                "depth": "1",
                "user": "",
            },
            "group": {
                "name": "",
                "description": "",
                "max_results": "unset",
                "max_scan_rows": "unset",
                "max_lock_time": "unset",
                "max_open_files": "unset",
                "timeout": "43200",
                "password_timeout": "unset",
                "subgroups": "",
                "owners": "",
                "users": "",
            },
            "user": {
                "name": "",
                "email": "",
                "full_name": "",
                "auth_method": "",
                "reviews": "",
                "job_view": "",
            },
            "stream": {
                "name": "",
                "type": "mainline",
                "depot": "",
                "user": os.getenv("P4USER"),
                "view": "inherit",
                "parent": "",
                "options": "allsubmit unlocked notoparent nofromparent mergedown",
            },
            "protection": {
                "access": "",
                "type": "",
                "name": "",
                "host": "*",
                "path": "",
                "comment": "",
            },
            "branch": {"name": "", "owner": "", "options": "unlocked"},
        }

        self.create_ui_elements()
        self.add_ui_elements_to_layout()
        self.connect_ui()
        self.set_window_settings()

        self.populate_data()
        self.exec()

    def create_ui_elements(self):
        self.btn_reload = QPushButton("Reload")
        self.btn_save = QPushButton("Save")

        self.main_tab_widget = QTabWidget()

        self.depot_tab = QWidget()

        self.depot_list = QListWidget()
        self.add_depot_btn = QPushButton("+")
        self.remove_depot_btn = QPushButton("-")
        self.depot_table = QTableWidget()

        self.depot_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.depot_table.horizontalHeader().setVisible(False)
        self.depot_table.verticalHeader().setVisible(False)
        self.depot_table.setColumnCount(2)
        self.depot_table.setRowCount(4)

        self.stream_tab = QWidget()
        self.stream_list = QListWidget()
        self.add_stream_btn = QPushButton("+")
        self.remove_stream_btn = QPushButton("-")
        self.stream_table = QTableWidget()

        self.stream_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.stream_table.horizontalHeader().setVisible(False)
        self.stream_table.verticalHeader().setVisible(False)
        self.stream_table.setColumnCount(2)
        self.stream_table.setRowCount(7)

        self.stream_view_tab_widget = QTabWidget()

        self.stream_paths_tab = QWidget()
        self.stream_paths_table = QTableWidget()
        self.stream_paths_table.setColumnCount(1)
        self.stream_paths_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.stream_paths_table.horizontalHeader().setVisible(False)
        self.stream_paths_table.verticalHeader().setVisible(False)

        self.stream_remapped_tab = QWidget()
        self.stream_remapped_table = QTableWidget()
        self.stream_remapped_table.setColumnCount(1)
        self.stream_remapped_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.stream_remapped_table.horizontalHeader().setVisible(False)
        self.stream_remapped_table.verticalHeader().setVisible(False)

        self.stream_ignored_tab = QWidget()
        self.stream_ignored_table = QTableWidget()
        self.stream_ignored_table.setColumnCount(1)
        self.stream_ignored_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.stream_ignored_table.horizontalHeader().setVisible(False)
        self.stream_ignored_table.verticalHeader().setVisible(False)

        self.group_tab = QWidget()
        self.group_list = QListWidget()
        self.add_group_btn = QPushButton("+")
        self.remove_group_btn = QPushButton("-")
        self.group_table = QTableWidget()

        self.group_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.group_table.horizontalHeader().setVisible(False)
        self.group_table.verticalHeader().setVisible(False)
        self.group_table.setColumnCount(2)
        self.group_table.setRowCount(11)

        self.user_tab = QWidget()
        self.user_list = QListWidget()
        self.add_user_btn = QPushButton("+")
        self.remove_user_btn = QPushButton("-")
        self.user_table = QTableWidget()

        self.user_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.user_table.horizontalHeader().setVisible(False)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setColumnCount(2)
        self.user_table.setRowCount(6)

        self.protection_tab = QWidget()
        self.protection_list = QListWidget()
        self.add_protection_btn = QPushButton("+")
        self.remove_protection_btn = QPushButton("-")
        self.protection_table = QTableWidget()

        self.protection_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.protection_table.horizontalHeader().setVisible(False)
        self.protection_table.verticalHeader().setVisible(False)
        self.protection_table.setColumnCount(2)
        self.protection_table.setRowCount(6)

        self.typemap_tab = QWidget()
        self.typemap_type_list = QListWidget()
        self.add_type_btn = QPushButton("+")
        self.edit_type_btn = QPushButton("…")
        self.remove_type_btn = QPushButton("-")
        self.typemap_path_table = QTableWidget()

        self.typemap_path_table.setColumnCount(1)
        self.typemap_path_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.typemap_path_table.horizontalHeader().setVisible(False)
        self.typemap_path_table.verticalHeader().setVisible(False)

        self.branch_tab = QWidget()
        self.branch_list = QListWidget()
        self.add_branch_btn = QPushButton("+")
        self.remove_branch_btn = QPushButton("-")
        self.branch_table = QTableWidget()
        self.branch_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.branch_table.horizontalHeader().setVisible(False)
        self.branch_table.verticalHeader().setVisible(False)
        self.branch_table.setColumnCount(2)
        self.branch_table.setRowCount(3)

        self.branch_view_table = QTableWidget()
        self.branch_view_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.branch_view_table.horizontalHeader().setVisible(False)
        self.branch_view_table.verticalHeader().setVisible(False)
        self.branch_view_table.setColumnCount(2)

    def add_ui_elements_to_layout(self):
        # Depot Tab
        self.depot_hlayout = QHBoxLayout()
        self.depot_btn_hlayout = QHBoxLayout()
        self.depot_vlayout = QVBoxLayout()

        self.depot_vlayout.addWidget(self.depot_list)
        self.depot_btn_hlayout.addWidget(self.remove_depot_btn)
        self.depot_btn_hlayout.addWidget(self.add_depot_btn)
        self.depot_vlayout.addLayout(self.depot_btn_hlayout)
        self.depot_hlayout.addLayout(self.depot_vlayout)
        self.depot_hlayout.addWidget(self.depot_table)
        self.depot_tab.setLayout(self.depot_hlayout)

        # Streams Tab
        self.stream_vlayout_main = QVBoxLayout()
        self.stream_hlayout = QHBoxLayout()
        self.stream_btn_hlayout = QHBoxLayout()
        self.stream_vlayout = QVBoxLayout()

        self.stream_vlayout.addWidget(self.stream_list)
        self.stream_btn_hlayout.addWidget(self.remove_stream_btn)
        self.stream_btn_hlayout.addWidget(self.add_stream_btn)
        self.stream_vlayout.addLayout(self.stream_btn_hlayout)
        self.stream_hlayout.addLayout(self.stream_vlayout)
        self.stream_hlayout.addWidget(self.stream_table)

        self.stream_vlayout_main.addLayout(self.stream_hlayout)
        self.stream_vlayout_main.addWidget(self.stream_view_tab_widget)

        self.stream_paths_tab_vlayout = QVBoxLayout()
        self.stream_paths_tab_vlayout.addWidget(self.stream_paths_table)
        self.stream_paths_tab.setLayout(self.stream_paths_tab_vlayout)
        self.stream_view_tab_widget.addTab(self.stream_paths_tab, "Paths")

        self.stream_remapped_tab_vlayout = QVBoxLayout()
        self.stream_remapped_tab_vlayout.addWidget(self.stream_remapped_table)
        self.stream_remapped_tab.setLayout(self.stream_remapped_tab_vlayout)
        self.stream_view_tab_widget.addTab(self.stream_remapped_tab, "Remapped")

        self.stream_ignored_tab_vlayout = QVBoxLayout()
        self.stream_ignored_tab_vlayout.addWidget(self.stream_ignored_table)
        self.stream_ignored_tab.setLayout(self.stream_ignored_tab_vlayout)
        self.stream_view_tab_widget.addTab(self.stream_ignored_tab, "Ignored")

        self.stream_tab.setLayout(self.stream_vlayout_main)

        # Group Tab
        self.group_hlayout = QHBoxLayout()
        self.group_btn_hlayout = QHBoxLayout()
        self.group_vlayout = QVBoxLayout()

        self.group_vlayout.addWidget(self.group_list)
        self.group_btn_hlayout.addWidget(self.remove_group_btn)
        self.group_btn_hlayout.addWidget(self.add_group_btn)
        self.group_vlayout.addLayout(self.group_btn_hlayout)
        self.group_hlayout.addLayout(self.group_vlayout)
        self.group_hlayout.addWidget(self.group_table)
        self.group_tab.setLayout(self.group_hlayout)

        # User Tab
        self.user_hlayout = QHBoxLayout()
        self.user_btn_hlayout = QHBoxLayout()
        self.user_vlayout = QVBoxLayout()

        self.user_vlayout.addWidget(self.user_list)
        self.user_btn_hlayout.addWidget(self.remove_user_btn)
        self.user_btn_hlayout.addWidget(self.add_user_btn)
        self.user_vlayout.addLayout(self.user_btn_hlayout)
        self.user_hlayout.addLayout(self.user_vlayout)
        self.user_hlayout.addWidget(self.user_table)
        self.user_tab.setLayout(self.user_hlayout)

        # Protection Tab
        self.protection_hlayout = QHBoxLayout()
        self.protection_btn_hlayout = QHBoxLayout()
        self.protection_vlayout = QVBoxLayout()

        self.protection_vlayout.addWidget(self.protection_list)
        self.protection_btn_hlayout.addWidget(self.remove_protection_btn)
        self.protection_btn_hlayout.addWidget(self.add_protection_btn)
        self.protection_vlayout.addLayout(self.protection_btn_hlayout)
        self.protection_hlayout.addLayout(self.protection_vlayout)
        self.protection_hlayout.addWidget(self.protection_table)
        self.protection_tab.setLayout(self.protection_hlayout)

        # typemap Tab
        self.typemap_hlayout = QHBoxLayout()
        self.typemap_type_vlayout = QVBoxLayout()
        self.typemap_path_vlayout = QVBoxLayout()
        self.type_btn_hlayout = QHBoxLayout()

        self.type_btn_hlayout.addWidget(self.add_type_btn)
        self.type_btn_hlayout.addWidget(self.edit_type_btn)
        self.type_btn_hlayout.addWidget(self.remove_type_btn)

        self.typemap_type_vlayout.addWidget(self.typemap_type_list)
        self.typemap_type_vlayout.addLayout(self.type_btn_hlayout)
        self.typemap_path_vlayout.addWidget(self.typemap_path_table)

        self.typemap_hlayout.addLayout(self.typemap_type_vlayout)
        self.typemap_hlayout.addLayout(self.typemap_path_vlayout)
        self.typemap_tab.setLayout(self.typemap_hlayout)

        # branch Tab
        self.branch_hlayout = QHBoxLayout()
        self.branch_btn_hlayout = QHBoxLayout()
        self.branch_vlayout = QVBoxLayout()
        self.branch_vlayout_main = QVBoxLayout()

        self.branch_vlayout.addWidget(self.branch_list)
        self.branch_btn_hlayout.addWidget(self.remove_branch_btn)
        self.branch_btn_hlayout.addWidget(self.add_branch_btn)
        self.branch_vlayout.addLayout(self.branch_btn_hlayout)
        self.branch_hlayout.addLayout(self.branch_vlayout)
        self.branch_hlayout.addWidget(self.branch_table)

        self.branch_vlayout_main.addLayout(self.branch_hlayout)
        self.branch_vlayout_main.addWidget(self.branch_view_table)
        self.branch_tab.setLayout(self.branch_vlayout_main)

        # Main Layout
        self.main_layout = QVBoxLayout()

        self.main_btn_row = QHBoxLayout()
        self.main_btn_row.addWidget(self.btn_reload)
        self.main_btn_row.addWidget(self.btn_save)

        self.main_tab_widget.addTab(self.depot_tab, "Depots")
        self.main_tab_widget.addTab(self.stream_tab, "Streams")
        self.main_tab_widget.addTab(self.group_tab, "Groups")
        self.main_tab_widget.addTab(self.user_tab, "Users")
        self.main_tab_widget.addTab(self.protection_tab, "Protections")
        self.main_tab_widget.addTab(self.typemap_tab, "Typemap")
        self.main_tab_widget.addTab(self.branch_tab, "Branches")
        self.main_layout.addWidget(self.main_tab_widget)
        self.main_layout.addLayout(self.main_btn_row)

        self.setLayout(self.main_layout)

    def set_window_settings(self):
        self.setWindowTitle("P4 Template Editor")
        self.setMinimumSize(400, 500)

    def connect_ui(self):
        self.depot_list.currentItemChanged.connect(self.reload_selected_depot_data)
        self.stream_list.currentItemChanged.connect(self.reload_selected_stream_data)
        self.group_list.currentItemChanged.connect(self.reload_selected_group_data)
        self.user_list.currentItemChanged.connect(self.reload_selected_user_data)
        self.protection_list.currentItemChanged.connect(
            self.reload_selected_protection_data
        )
        self.typemap_path_table.cellChanged.connect(
            self.update_current_typemap_path_data
        )
        self.typemap_type_list.currentItemChanged.connect(
            self.reload_selected_typemap_data
        )
        self.branch_list.currentItemChanged.connect(self.reload_selected_branch_data)

        self.add_depot_btn.clicked.connect(self.add_new_depot)
        self.remove_depot_btn.clicked.connect(self.remove_depot)
        self.depot_table.cellChanged.connect(self.update_current_depot_data)

        self.add_stream_btn.clicked.connect(self.add_new_stream)
        self.remove_stream_btn.clicked.connect(self.remove_stream)
        self.stream_table.cellChanged.connect(self.update_current_stream_data)
        self.stream_paths_table.cellChanged.connect(
            self.update_current_stream_path_data
        )
        self.stream_remapped_table.cellChanged.connect(
            self.update_current_stream_remapped_data
        )
        self.stream_ignored_table.cellChanged.connect(
            self.update_current_stream_ignored_data
        )

        self.add_group_btn.clicked.connect(self.add_new_group)
        self.remove_group_btn.clicked.connect(self.remove_group)
        self.group_table.cellChanged.connect(self.update_current_group_data)

        self.add_user_btn.clicked.connect(self.add_new_user)
        self.remove_user_btn.clicked.connect(self.remove_user)
        self.user_table.cellChanged.connect(self.update_current_user_data)

        self.add_protection_btn.clicked.connect(self.add_new_protection)
        self.remove_protection_btn.clicked.connect(self.remove_protection)

        self.add_branch_btn.clicked.connect(self.add_new_branch)
        self.remove_branch_btn.clicked.connect(self.remove_branch)
        self.protection_table.cellChanged.connect(self.update_current_protection_data)

        self.branch_view_table.cellChanged.connect(self.update_current_branch_view_data)
        self.branch_table.cellChanged.connect(self.update_current_branch_data)

        self.btn_save.clicked.connect(self.save_data)
        self.btn_reload.clicked.connect(self.populate_data)

        self.add_type_btn.clicked.connect(self.add_typemap_type)
        self.edit_type_btn.clicked.connect(self.edit_typemap_type)
        self.remove_type_btn.clicked.connect(self.remove_typemap_type)

    def populate_data(self):
        self.template_data = {}
        if self.template_path and os.path.isfile(self.template_path):
            self.template_data = read_json(self.template_path)

        self.populate_depot_data()
        self.populate_group_data()
        self.populate_user_data()
        self.populate_stream_data()
        self.populate_protection_data()
        self.populate_typemap_data()
        self.populate_branch_data()

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", self.template_path, "Text Files(*.json)"
        )
        print(file_name)
        if file_name:
            write_json(self.template_data, file_name)

    # DEPOTS
    def populate_depot_data(self):
        self.item_load = True
        self.depot_list.clear()
        if self.template_data.get("depots"):
            for depot in self.template_data["depots"]:
                self.depot_list.addItem(depot["name"])
            if self.depot_list.count():
                self.depot_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_depot_data(self):
        self.item_load = True
        self.depot_table.clear()

        if not self.template_data.get("depots", []):
            return

        depot_index = self.depot_list.currentRow()
        for i, key in enumerate(["name", "type", "depth", "user"]):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.depot_table.setItem(i, 0, key_item)
            self.depot_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["depots"][depot_index].get(
                            key, self.defaults["depot"][key]
                        )
                    )
                ),
            )
        self.item_load = False

    def add_new_depot(self):
        current_depotnames = [_["name"] for _ in self.template_data.get("depots", [])]
        i = 1
        depot_name = "NewDepot"

        if depot_name in current_depotnames:
            while depot_name + str(i) in current_depotnames:
                i += 1
            depot_name += str(i)

        if "depots" not in self.template_data:
            self.template_data["depots"] = []

        self.template_data["depots"].append({"name": depot_name})
        self.populate_depot_data()

    def remove_depot(self):
        if not self.depot_list.currentItem():
            return

        depot_name = self.depot_list.currentItem().text()
        self.template_data["depots"] = [
            _ for _ in self.template_data["depots"] if _["name"] != depot_name
        ]
        self.populate_depot_data()

    def update_current_depot_data(self):
        if self.item_load:
            return

        current_depot_name = self.depot_list.currentItem().text()
        current_depot = [
            _ for _ in self.template_data["depots"] if _["name"] == current_depot_name
        ]

        if not current_depot:
            return

        current_depot = current_depot[0]
        current_depot_index = self.template_data["depots"].index(current_depot)
        refresh_list = False

        for i in range(self.depot_table.rowCount()):
            if not self.depot_table.item(i, 0):
                continue

            depot_key = self.depot_table.item(i, 0).text().lower()
            depot_value = ""

            if self.depot_table.item(i, 1) and self.depot_table.item(i, 1).text():
                depot_value = self.depot_table.item(i, 1).text()

            if depot_key == "name" and not depot_value:
                continue

            if depot_key == "name" and depot_value != current_depot_name:
                refresh_list = True
            self.template_data["depots"][current_depot_index][depot_key] = depot_value

        if refresh_list:
            self.populate_depot_data()

    # GROUPS
    def populate_group_data(self):
        self.item_load = True
        self.group_list.clear()
        if self.template_data.get("groups"):
            for group in self.template_data["groups"]:
                self.group_list.addItem(group["name"])
            if self.group_list.count():
                self.group_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_group_data(self):
        self.item_load = True
        self.group_table.clear()
        group_index = self.group_list.currentRow()

        if not self.template_data.get("groups", []):
            return

        for i, key in enumerate(
            [
                "name",
                "description",
                "max_results",
                "max_scan_rows",
                "max_lock_time",
                "max_open_files",
                "timeout",
                "password_timeout",
                "subgroups",
                "owners",
                "users",
            ]
        ):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.group_table.setItem(i, 0, key_item)
            self.group_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["groups"][group_index].get(
                            key, self.defaults["group"][key]
                        ),
                        ", ",
                    )
                ),
            )
        self.item_load = False

    def add_new_group(self):
        current_groupnames = [_["name"] for _ in self.template_data.get("groups", [])]
        i = 1
        group_name = "NewGroup"

        if group_name in current_groupnames:
            while group_name + str(i) in current_groupnames:
                i += 1
            group_name += str(i)

        if "groups" not in self.template_data:
            self.template_data["groups"] = []

        self.template_data["groups"].append({"name": group_name})
        self.populate_group_data()

    def remove_group(self):
        if not self.group_list.currentItem():
            return

        group_name = self.group_list.currentItem().text()
        self.template_data["groups"] = [
            _ for _ in self.template_data["groups"] if _["name"] != group_name
        ]
        self.populate_group_data()

    def update_current_group_data(self):
        if self.item_load:
            return

        current_group_name = self.group_list.currentItem().text()
        current_group = [
            _ for _ in self.template_data["groups"] if _["name"] == current_group_name
        ]

        if not current_group:
            return

        current_group = current_group[0]
        current_group_index = self.template_data["groups"].index(current_group)
        refresh_list = False

        for i in range(self.group_table.rowCount()):
            if not self.group_table.item(i, 0):
                continue

            group_key = self.group_table.item(i, 0).text().lower()
            group_value = ""

            if self.group_table.item(i, 1) and self.group_table.item(i, 1).text():
                group_value = self.group_table.item(i, 1).text()

            if group_key == "name" and not group_value:
                continue

            if group_key == "name" and group_value != current_group_name:
                refresh_list = True
            self.template_data["groups"][current_group_index][group_key] = group_value

        if refresh_list:
            self.populate_group_data()

    # USERS
    def populate_user_data(self):
        self.item_load = True
        self.user_list.clear()
        if self.template_data.get("users"):
            for user in self.template_data["users"]:
                self.user_list.addItem(user["name"])
            if self.user_list.count():
                self.user_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_user_data(self):
        self.item_load = True
        self.user_table.clear()
        user_index = self.user_list.currentRow()

        if not self.template_data.get("users", []):
            return

        for i, key in enumerate(
            ["name", "email", "full_name", "auth_method", "reviews", "job_view"]
        ):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(i, 0, key_item)
            self.user_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["users"][user_index].get(
                            key, self.defaults["user"][key]
                        ),
                        ", ",
                    )
                ),
            )
        self.item_load = False

    def add_new_user(self):
        current_usernames = [_["name"] for _ in self.template_data.get("users", [])]
        i = 1
        user_name = "NewUser"

        if user_name in current_usernames:
            while user_name + str(i) in current_usernames:
                i += 1
            user_name += str(i)

        if "users" not in self.template_data:
            self.template_data["users"] = []

        self.template_data["users"].append({"name": user_name})
        self.populate_user_data()

    def remove_user(self):
        if not self.user_list.currentItem():
            return

        user_name = self.user_list.currentItem().text()
        self.template_data["users"] = [
            _ for _ in self.template_data["users"] if _["name"] != user_name
        ]
        self.populate_user_data()

    def update_current_user_data(self):
        if self.item_load:
            return

        current_user_name = self.user_list.currentItem().text()
        current_user = [
            _ for _ in self.template_data["users"] if _["name"] == current_user_name
        ]

        if not current_user:
            return

        current_user = current_user[0]
        current_user_index = self.template_data["users"].index(current_user)
        refresh_list = False

        for i in range(self.user_table.rowCount()):
            if not self.user_table.item(i, 0):
                continue

            user_key = self.user_table.item(i, 0).text().lower()
            user_value = ""

            if self.user_table.item(i, 1) and self.user_table.item(i, 1).text():
                user_value = self.user_table.item(i, 1).text()

            if user_key == "name" and not user_value:
                continue

            if user_key == "name" and user_value != current_user_name:
                refresh_list = True

            self.template_data["users"][current_user_index][user_key] = user_value

        if refresh_list:
            self.populate_user_data()

    # STREAMS
    def populate_stream_data(self):
        self.item_load = True
        self.stream_list.clear()
        if self.template_data.get("streams"):
            for stream in self.template_data["streams"]:
                self.stream_list.addItem(stream["name"])
            if self.stream_list.count():
                self.stream_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_stream_data(self):
        self.item_load = True
        self.stream_table.clear()
        self.stream_paths_table.clear()
        self.stream_remapped_table.clear()
        self.stream_ignored_table.clear()

        if not self.template_data.get("streams", []):
            return

        stream_index = self.stream_list.currentRow()
        for i, key in enumerate(
            ["name", "type", "depot", "user", "view", "parent", "options"]
        ):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.stream_table.setItem(i, 0, key_item)
            self.stream_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["streams"][stream_index].get(
                            key, self.defaults["stream"][key]
                        ),
                        " ",
                    )
                ),
            )

        path_values = self.template_data["streams"][stream_index].get("paths", [])
        self.stream_paths_table.setRowCount(len(path_values) + 1)
        for i, path_value in enumerate(path_values):
            self.stream_paths_table.setItem(
                i,
                0,
                QTableWidgetItem(
                    path_value,
                ),
            )

        remapped_values = self.template_data["streams"][stream_index].get(
            "remapped", []
        )
        self.stream_remapped_table.setRowCount(len(remapped_values) + 1)
        for i, remapped_value in enumerate(remapped_values):
            self.stream_remapped_table.setItem(
                i,
                0,
                QTableWidgetItem(
                    remapped_value,
                ),
            )

        ignored_values = self.template_data["streams"][stream_index].get("ignored", [])
        self.stream_ignored_table.setRowCount(len(ignored_values) + 1)
        for i, ignored_value in enumerate(ignored_values):
            self.stream_ignored_table.setItem(
                i,
                0,
                QTableWidgetItem(
                    ignored_value,
                ),
            )

        self.item_load = False

    def add_new_stream(self):
        current_stream_names = [
            _["name"] for _ in self.template_data.get("streams", [])
        ]
        i = 1
        stream_name = "NewStream"

        if stream_name in current_stream_names:
            while stream_name + str(i) in current_stream_names:
                i += 1
            stream_name += str(i)

        if "streams" not in self.template_data:
            self.template_data["streams"] = []

        self.template_data["streams"].append({"name": stream_name})
        self.populate_stream_data()

    def remove_stream(self):
        if not self.stream_list.currentItem():
            return

        stream_name = self.stream_list.currentItem().text()
        self.template_data["streams"] = [
            _ for _ in self.template_data["streams"] if _["name"] != stream_name
        ]
        self.populate_stream_data()

    def update_current_stream_data(self):
        if self.item_load:
            return

        current_stream_name = self.stream_list.currentItem().text()
        current_stream = [
            _ for _ in self.template_data["streams"] if _["name"] == current_stream_name
        ]

        if not current_stream:
            return

        current_stream = current_stream[0]
        current_stream_index = self.template_data["streams"].index(current_stream)
        refresh_list = False

        for i in range(self.stream_table.rowCount()):
            if not self.stream_table.item(i, 0):
                continue

            stream_key = self.stream_table.item(i, 0).text().lower()
            stream_value = ""

            if self.stream_table.item(i, 1) and self.stream_table.item(i, 1).text():
                stream_value = self.stream_table.item(i, 1).text()

            if stream_key == "name" and not stream_value:
                continue

            if stream_key == "name" and stream_value != current_stream_name:
                refresh_list = True

            self.template_data["streams"][current_stream_index][
                stream_key
            ] = stream_value

        if refresh_list:
            self.populate_stream_data()

    def update_current_stream_path_data(self):
        if self.item_load:
            return

        current_stream_name = self.stream_list.currentItem().text()
        current_stream = [
            _ for _ in self.template_data["streams"] if _["name"] == current_stream_name
        ]

        if not current_stream:
            return

        current_stream = current_stream[0]
        current_stream_index = self.template_data["streams"].index(current_stream)

        table_values = []
        for i in range(self.stream_paths_table.rowCount()):
            if not self.stream_paths_table.item(i, 0):
                continue

            path_value = self.stream_paths_table.item(i, 0).text()

            if path_value:
                table_values.append(path_value)

        if table_values:
            self.template_data["streams"][current_stream_index]["paths"] = table_values

        print(
            len(self.template_data["streams"][current_stream_index].get("paths", [])),
            self.template_data["streams"][current_stream_index].get("paths", []),
        )
        self.stream_paths_table.setRowCount(
            len(self.template_data["streams"][current_stream_index].get("paths", []))
            + 1
        )

    def update_current_stream_remapped_data(self):
        if self.item_load:
            return

        current_stream_name = self.stream_list.currentItem().text()
        current_stream = [
            _ for _ in self.template_data["streams"] if _["name"] == current_stream_name
        ]

        if not current_stream:
            return

        current_stream = current_stream[0]
        current_stream_index = self.template_data["streams"].index(current_stream)

        table_values = []
        for i in range(self.stream_remapped_table.rowCount()):
            if not self.stream_remapped_table.item(i, 0):
                continue

            remapped_value = self.stream_remapped_table.item(i, 0).text()

            if remapped_value:
                table_values.append(remapped_value)

        if table_values:
            self.template_data["streams"][current_stream_index][
                "remapped"
            ] = table_values

        print(
            len(
                self.template_data["streams"][current_stream_index].get("remapped", [])
            ),
            self.template_data["streams"][current_stream_index].get("remapped", []),
        )
        self.stream_remapped_table.setRowCount(
            len(self.template_data["streams"][current_stream_index].get("remapped", []))
            + 1
        )

    def update_current_stream_ignored_data(self):
        if self.item_load:
            return

        current_stream_name = self.stream_list.currentItem().text()
        current_stream = [
            _ for _ in self.template_data["streams"] if _["name"] == current_stream_name
        ]

        if not current_stream:
            return

        current_stream = current_stream[0]
        current_stream_index = self.template_data["streams"].index(current_stream)

        table_values = []
        for i in range(self.stream_ignored_table.rowCount()):
            if not self.stream_ignored_table.item(i, 0):
                continue

            ignored_value = self.stream_ignored_table.item(i, 0).text()

            if ignored_value:
                table_values.append(ignored_value)

        if table_values:
            self.template_data["streams"][current_stream_index][
                "ignored"
            ] = table_values

        print(
            len(self.template_data["streams"][current_stream_index].get("ignored", [])),
            self.template_data["streams"][current_stream_index].get("ignored", []),
        )
        self.stream_ignored_table.setRowCount(
            len(self.template_data["streams"][current_stream_index].get("ignored", []))
            + 1
        )

    # PROTECTIONS
    def populate_protection_data(self):
        self.item_load = True
        self.protection_list.clear()
        if self.template_data.get("protections"):
            for protection in self.template_data["protections"]:
                self.protection_list.addItem(protection["name"])
            if self.protection_list.count():
                self.protection_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_protection_data(self):
        self.item_load = True
        self.protection_table.clear()
        protection_index = self.protection_list.currentRow()

        if not self.template_data.get("protections", []):
            return

        for i, key in enumerate(["access", "type", "name", "host", "path", "comment"]):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.protection_table.setItem(i, 0, key_item)
            self.protection_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["protections"][protection_index].get(
                            key, self.defaults["protection"][key]
                        ),
                        " ",
                    )
                ),
            )
        self.item_load = False

    def add_new_protection(self):
        current_protection_names = [
            _["name"] for _ in self.template_data.get("protections", [])
        ]
        i = 1
        protection_name = "NewProtection"

        if protection_name in current_protection_names:
            while protection_name + str(i) in current_protection_names:
                i += 1
            protection_name += str(i)

        if "protections" not in self.template_data:
            self.template_data["protections"] = []

        self.template_data["protections"].append({"name": protection_name})
        self.populate_protection_data()

    def remove_protection(self):
        if not self.protection_list.currentItem():
            return

        protection_name = self.protection_list.currentItem().text()
        self.template_data["protections"] = [
            _ for _ in self.template_data["protections"] if _["name"] != protection_name
        ]
        self.populate_protection_data()

    def update_current_protection_data(self):
        if self.item_load:
            return

        current_protection_name = self.protection_list.currentItem().text()
        current_protection = [
            _
            for _ in self.template_data["protections"]
            if _["name"] == current_protection_name
        ]

        if not current_protection:
            return

        current_protection = current_protection[0]
        current_protection_index = self.template_data["protections"].index(
            current_protection
        )
        refresh_list = False

        for i in range(self.protection_table.rowCount()):
            if not self.protection_table.item(i, 0):
                continue

            protection_key = self.protection_table.item(i, 0).text().lower()
            protection_value = ""

            if (
                self.protection_table.item(i, 1)
                and self.protection_table.item(i, 1).text()
            ):
                protection_value = self.protection_table.item(i, 1).text()

            if protection_key == "name" and not protection_value:
                continue

            if protection_key == "name" and protection_value != current_protection_name:
                refresh_list = True

            self.template_data["protections"][current_protection_index][
                protection_key
            ] = protection_value

        if refresh_list:
            self.populate_protection_data()

    # TYPEMAP
    def populate_typemap_data(self):
        self.item_load = True
        self.typemap_type_list.clear()
        self.typemap_path_table.clear()
        if self.template_data.get("types"):
            sorted_types = sorted(self.template_data["types"].keys())
            for typemap in sorted_types:
                self.typemap_type_list.addItem(typemap)
            self.typemap_type_list.setCurrentRow(0)
        self.item_load = False

    def add_typemap_type(self):
        current_types = sorted(self.template_data.get("types", {}).keys())
        i = 1
        type_name = GetTypeNameDialog().type_name

        if not type_name:
            return

        if type_name in current_types:
            while type_name + str(i) in current_types:
                i += 1
            type_name += str(i)

        if "types" not in self.template_data:
            self.template_data["types"] = {}

        self.template_data["types"][type_name] = []

        self.populate_typemap_data()

    def remove_typemap_type(self):
        if not self.typemap_type_list.currentItem():
            return

        type_name = self.typemap_type_list.currentItem().text()
        if type_name in self.template_data["types"]:
            del self.template_data["types"][type_name]

        self.populate_typemap_data()

    def edit_typemap_type(self):
        if not self.typemap_type_list.currentItem():
            return

        type_name = self.typemap_type_list.currentItem().text()

        new_type_name = GetTypeNameDialog(type_name=type_name).type_name

        if not new_type_name:
            return

        if new_type_name and new_type_name != type_name:
            self.template_data["types"][new_type_name] = self.template_data["types"][
                type_name
            ]
            del self.template_data["types"][type_name]

        self.populate_typemap_data()

    def reload_selected_typemap_data(self):
        self.item_load = True
        self.typemap_path_table.clear()

        current_type = self.typemap_type_list.currentItem()
        if not current_type:
            return
        current_type = current_type.text()

        path_values = self.template_data["types"].get(current_type, [])
        self.typemap_path_table.setRowCount(len(path_values) + 1)
        for i, path_value in enumerate(path_values):
            self.typemap_path_table.setItem(
                i,
                0,
                QTableWidgetItem(
                    path_value,
                ),
            )

        self.item_load = False

    def update_current_typemap_path_data(self):
        if self.item_load:
            return

        current_type = self.typemap_type_list.currentItem().text()

        current_type_data = self.template_data["types"].get(current_type, [])

        table_values = set()
        for i in range(self.typemap_path_table.rowCount()):
            if not self.typemap_path_table.item(i, 0):
                continue

            path_value = self.typemap_path_table.item(i, 0).text()

            if path_value:
                table_values.add(path_value)

        if table_values:
            self.template_data["types"][current_type] = sorted(table_values)

        self.typemap_path_table.setRowCount(
            len(self.template_data["types"].get(current_type, [])) + 1
        )

    # BRANCHES
    def populate_branch_data(self):
        self.item_load = True
        self.branch_list.clear()
        if self.template_data.get("branches"):
            for branch in self.template_data["branches"]:
                self.branch_list.addItem(branch["name"])
            if self.branch_list.count():
                self.branch_list.setCurrentRow(0)
        self.item_load = False

    def reload_selected_branch_data(self):
        self.item_load = True
        self.branch_table.clear()
        self.branch_view_table.clear()

        branch_index = self.branch_list.currentRow()
        if not self.template_data.get("branches", []):
            return

        for i, key in enumerate(["name", "owner", "options"]):
            key_item = QTableWidgetItem(key.capitalize())
            key_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.branch_table.setItem(i, 0, key_item)
            self.branch_table.setItem(
                i,
                1,
                QTableWidgetItem(
                    convert_to_string(
                        self.template_data["branches"][branch_index].get(
                            key, self.defaults["branch"][key]
                        )
                    )
                ),
            )

        self.branch_view_table.setRowCount(
            len(self.template_data["branches"][branch_index].get("view", {})) + 1
        )

        for i, item in enumerate(
            self.template_data["branches"][branch_index].get("view", {}).items()
        ):
            self.branch_view_table.setItem(i, 0, QTableWidgetItem(item[0]))
            self.branch_view_table.setItem(i, 1, QTableWidgetItem(item[1]))
        self.item_load = False

    def add_new_branch(self):
        current_branch_names = [
            _["name"] for _ in self.template_data.get("branches", [])
        ]
        i = 1
        branch_name = "NewBranch"

        if branch_name in current_branch_names:
            while branch_name + str(i) in current_branch_names:
                i += 1
            branch_name += str(i)

        if "branches" not in self.template_data:
            self.template_data["branches"] = []

        self.template_data["branches"].append({"name": branch_name})
        self.populate_branch_data()

    def remove_branch(self):
        if not self.branch_list.currentItem():
            return

        branch_name = self.branch_list.currentItem().text()
        self.template_data["branches"] = [
            _ for _ in self.template_data["branches"] if _["name"] != branch_name
        ]
        self.populate_branch_data()

    def update_current_branch_data(self):
        if self.item_load:
            return

        current_branch_name = self.branch_list.currentItem().text()
        current_branch = [
            _
            for _ in self.template_data["branches"]
            if _["name"] == current_branch_name
        ]

        if not current_branch:
            return

        current_branch = current_branch[0]
        current_branch_index = self.template_data["branches"].index(current_branch)
        refresh_list = False

        for i in range(self.branch_table.rowCount()):
            if not self.branch_table.item(i, 0):
                continue

            branch_key = self.branch_table.item(i, 0).text().lower()
            branch_value = ""

            if self.branch_table.item(i, 1) and self.branch_table.item(i, 1).text():
                branch_value = self.branch_table.item(i, 1).text()

            if branch_key == "options":
                branch_value = branch_value.split(" ")

            if branch_key == "name" and not branch_value:
                continue

            if branch_key == "name" and branch_value != current_branch_name:
                refresh_list = True

            self.template_data["branches"][current_branch_index][
                branch_key
            ] = branch_value

        if refresh_list:
            self.populate_branch_data()

    def update_current_branch_view_data(self):
        if self.item_load:
            return
        current_branch_name = self.branch_list.currentItem().text()

        current_branch = [
            _
            for _ in self.template_data["branches"]
            if _["name"] == current_branch_name
        ]
        if not current_branch:
            return
        current_branch = current_branch[0]
        current_branch_index = self.template_data["branches"].index(current_branch)

        # Views
        branch_view_dict = {}
        for i in range(self.branch_view_table.rowCount()):
            if (
                self.branch_view_table.item(i, 0)
                and self.branch_view_table.item(i, 0).text()
            ):
                view_value = ""
                if (
                    self.branch_view_table.item(i, 1)
                    and self.branch_view_table.item(i, 1).text()
                ):
                    view_value = self.branch_view_table.item(i, 1).text()
                branch_view_dict[self.branch_view_table.item(i, 0).text()] = view_value

        self.template_data["branches"][current_branch_index]["view"] = branch_view_dict

        self.branch_view_table.setRowCount(
            len(self.template_data["branches"][current_branch_index].get("view", {}))
            + 1
        )
