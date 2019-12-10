"""
An example of dialog in which users input data

MUEI- Medical Images
Dani Tost- 2019
"""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QPushButton, QColorDialog, QVBoxLayout, QCheckBox

class SphereDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self) :
        grid = QGridLayout()
        grid.addWidget(QLabel('Center x:'), 0, 0)
        self.x = QLineEdit()
        grid.addWidget(self.x, 0, 1)
        grid.addWidget(QLabel('Center y:'), 0, 2)
        self.y = QLineEdit()
        grid.addWidget(self.y, 0, 3)
        grid.addWidget(QLabel('Center z:'), 0, 4)
        self.z = QLineEdit()
        grid.addWidget(self.z, 0, 5)
        grid.addWidget(QLabel('Radius:'), 1, 0)
        self.radius = QLineEdit()
        grid.addWidget(self.radius, 1, 1)
        grid.addWidget(QLabel('Theta res.:'), 2, 0)
        self.resh = QLineEdit()
        grid.addWidget(self.resh, 2, 1)
        grid.addWidget(QLabel('Phi res.:'), 2, 2)
        self.resv= QLineEdit()
        grid.addWidget(self.resv, 2, 3)

        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)
        
