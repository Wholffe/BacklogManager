from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class CategoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/backlog_manager_add_cat.ui',self)

    def get_content(self):
        return self.new_category_input.text()