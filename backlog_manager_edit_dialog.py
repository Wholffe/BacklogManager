from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class CreateBacklogDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/backlogmanager_edit_dialog.ui',self)

    def get_content(self):
        content = []
        content.append(self.lineEditTitel.text())
        content.append(self.lineEditKurzbeschreibung.text())
        return content
