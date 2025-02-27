from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from config_handler import fetch_all_categories


class BacklogDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/backlog_manager_edit_dialog.ui',self)
        self.input_type.addItems(fetch_all_categories())
        self.input_status.addItems(['Auf der Watchlist', 'Gerade dran', 'Erledigt'])

    def get_content(self):
        content = []
        content.append(self.lineEditTitel.text())
        content.append(self.lineEditKurzbeschreibung.text())
        return content
