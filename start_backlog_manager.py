import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QLabel, QVBoxLayout, QScrollArea, QProgressBar
import os

from backlog_manager_edit_dialog import BacklogDialog
from backlog_manager_add_cat import CategoryDialog

from config_handler import fetch_all_categories, fetch_backlogs_from_categories, append_to_backlog_config


class BacklogManager(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/backlog_manager_main.ui", self)
        self.show()

        self.initialize_program_data()
        self.populate_ui_element_data()

        self.align_table_headers()
        self.setup_menu_actions()

    def add_new_backlog(self):
        backlog_dialog = BacklogDialog()
        backlog_dialog.exec()

        _name = backlog_dialog.input_name.text()
        _type = str(backlog_dialog.input_type.currentText())                   # category
        _description = str(backlog_dialog.input_description.text())
        _status = str(backlog_dialog.input_status.currentText())
        _progress = str(backlog_dialog.input_progress.value())    
        _notes = backlog_dialog.textedit_notes.toPlainText()

        category_name = _type.lower().replace(" ", "_")
        append_to_backlog_config(category_name, [_name, _type, _description, _status, _progress, _notes])


    def add_new_backlog_row(self, backlog):
        _type, _name, _description, _status, _progress, _notes = backlog

        row_count = self.backlog_collection_table.rowCount()
        self.backlog_collection_table.insertRow(row_count)
        self.backlog_collection_table.setItem(row_count, 0, QTableWidgetItem(row_count))
        self.backlog_collection_table.setItem(row_count, 1, QTableWidgetItem(_type))
        self.backlog_collection_table.setItem(row_count, 2, QTableWidgetItem(_name))
        self.backlog_collection_table.setItem(row_count, 3, QTableWidgetItem(_description))
        self.backlog_collection_table.setItem(row_count, 4, QTableWidgetItem(_status))


    def add_new_category(self):
        category_dialog = CategoryDialog()
        category_dialog.exec()

        new_category = category_dialog.new_category_input.text()   # Neue Spiele
        new_category.lower().replace(" ", "_")                     # neue_spiele

        with open("config/custom_categories.txt", "a+") as file:
            file.write(f"\n{new_category}")
            self.categories.append(new_category)


    def align_table_headers(self):
        pass

    def edit_backlog(self):
        pass

    def initialize_program_data(self):
        # read in categories
        self.categories = fetch_all_categories()
        self.backlogs = fetch_backlogs_from_categories(self.categories)

    def populate_ui_element_data(self):
        self.combobox_category_filter.addItems(self.categories)
        self.combobox_column_filter.addItems(["ID", "Titel", "Beschreibung", "Status"])

        # initialize the table
        for category in self.categories:
            for i, backlog in enumerate(self.backlogs[category]):
                self.add_new_backlog_row(backlog)

    def setup_menu_actions(self):
        self.action_new_backlog.triggered.connect(self.add_new_backlog)
        self.action_new_category.triggered.connect(self.add_new_category)
        self.action_edit_backlog.triggered.connect(self.edit_backlog)
        self.backlog_collection_table.cellClicked.connect(self.display_backlog_details)

    def display_backlog_details(self, row, column):
        self.backlog_collection_table.selectRow(row)
        _title = self.backlog_collection_table.item(row, 1).text()
        _category = str(self.combobox_category_filter.currentText())

        backlog = self.fetch_backlog_by_title_and_category(_title, _category)
        if backlog:
            _progress = int(backlog[4])
            _notes = backlog[5]

            scroll_area = self.findChild(QScrollArea, "scrollArea")
            scroll_area_widget = scroll_area.widget()
            layout = QVBoxLayout(scroll_area_widget)

            layout.addWidget(QLabel(f"Progress:"))
            progress_bar = QProgressBar()
            progress_bar.setValue(_progress)
            layout.addWidget(progress_bar)
            layout.addWidget(QLabel(f"Notes:\n {_notes}"))

            scroll_area_widget.setLayout(layout)

    def fetch_backlog_by_title_and_category(self, title, category) -> list:
        path = f"config/{category}.txt"
        if not os.path.exists(path):
            return None

        with open(path, "r") as file:
            for line in file:
                backlog = line.strip().split(";")
                if backlog[0] == title:
                    return backlog
        return None


app = QApplication(sys.argv)
main_window = BacklogManager()
sys.exit(app.exec())
