from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class InfoBoxWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/backlog_manager_infobox_widget.ui',self)
    
    def set_progress_value(self, value):
        self.progress_bar.setValue(value)
    
    def set_notes(self, notes):
        self.textedit_notes.setText(notes)
    
    def set_empty(self):
        self.progress_bar.setValue(0)
        self.textedit_notes.setText('')