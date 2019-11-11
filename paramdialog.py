"""
An example of dialog in which users input data
Here the resolution of an image is queried.

MUEI- Medical Images
Dani Tost- 2019
"""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QPushButton, QColorDialog

class ParamImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self) :
        grid = QGridLayout()
        grid.addWidget(QLabel('width'), 0, 0)
        self.width = QLineEdit()
        grid.addWidget(self.width, 0, 1)
        grid.addWidget(QLabel('height'), 1, 0)
        self.height = QLineEdit()
        grid.addWidget(self.height, 1, 1)
        grid.addWidget(QLabel('color'), 2, 0)
        color_button = QPushButton('Open color dialog', self)
        grid.addWidget(color_button, 2, 1)
        color = self.on_click_color_dialog
        color_button.clicked.connect(color)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

    def on_click_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color = str(color.name())
            color = color.lstrip('#')
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            self.color = color
