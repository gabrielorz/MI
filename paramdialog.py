"""
An example of dialog in which users input data
Here the resolution of an image is queried.

MUEI- Medical Images
Dani Tost- 2019
"""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QPushButton, QColorDialog, \
    QWidget, QButtonGroup, QCheckBox, QHBoxLayout


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
        self.color = None
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
            "color = str(color.name())"
            "color = color.lstrip('#')"
            "color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))"
            self.color = color.getRgb()
        else:
            self.color = None
            
class GaussianImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self) :
        grid = QGridLayout()
        grid.addWidget(QLabel('sigma'), 0, 0)
        self.sigma = QLineEdit()
        grid.addWidget(self.sigma, 0, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)


class ChambolleImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('Weight'), 0, 0)
        self.weight = QLineEdit()
        grid.addWidget(self.weight, 0, 1)
        grid.addWidget(QLabel('Epsilon'), 1, 0)
        self.epsilon = QLineEdit()
        grid.addWidget(self.epsilon, 1, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

class NoiseImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('sigma'), 0, 0)
        self.sigma = QLineEdit()
        grid.addWidget(self.sigma, 0, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

class UserThresholdImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('Threshold'), 0, 0)
        self.threshold = QLineEdit()
        grid.addWidget(self.threshold, 0, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)


class SobelImageDialog(QDialog):

    def __init__(self,parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """grid = QGridLayout()
        horizontal = QCheckBox('Horizontal')
        vertical = QCheckBox('Vertical')
        both = QCheckBox('Both')
        both.setChecked(True)
        box = QDialogButtonBox
        grid.addButton(horizontal)
        grid.addButton(vertical)
        grid.addButton(both)
        grid.addWidget(horizontal, 2, 0)
        grid.addWidget(vertical, 1, 0)
        grid.addWidget(both, 0, 0)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)"""
        grid = QGridLayout()
        grid.addWidget(QLabel('Both'), 0, 1)
        both = QCheckBox()
        grid.addWidget(both, 0, 0)
        grid.addWidget(QLabel('Horizontal'), 0, 3)
        horizontal = QCheckBox()
        grid.addWidget(horizontal, 0, 2)
        grid.addWidget(QLabel('Vertical'), 0, 5)
        vertical = QCheckBox()
        grid.addWidget(vertical, 0, 4)
        both.setChecked(True)
        choosesobel = QButtonGroup(self)
        choosesobel.addButton(both)
        choosesobel.addButton(horizontal)
        choosesobel.addButton(vertical)
        if horizontal.isChecked():
            self.direction = 'horizontal'
        elif vertical.isChecked():
            self.direction = 'vertical'
        else:
            self.direction = 'both'
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 10, 0, -1, -1)
        box.setWindowTitle("Sobel filter")
        self.setLayout(grid)

class ClipCircleImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('Radius'), 1, 0)
        self.radius = QLineEdit()
        grid.addWidget(self.radius, 1, 1)
        grid.addWidget(QLabel('Center'), 0, 0)
        self.centerx = QLineEdit()
        grid.addWidget(self.centerx, 0, 1)
        self.centery = QLineEdit()
        grid.addWidget(self.centery, 0, 2)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

class ContrastStretchImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self) :
        grid = QGridLayout()
        grid.addWidget(QLabel('Minimum Percentile'), 0, 0)
        self.pmin = QLineEdit()
        grid.addWidget(self.pmin, 0, 1)
        grid.addWidget(QLabel('Maximum Percentile'), 1, 0)
        self.pmax = QLineEdit()
        grid.addWidget(self.pmax, 1, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

class SaveImageDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self) :
        grid = QGridLayout()
        grid.addWidget(QLabel('Save as'), 0, 0)
        self.filename = QLineEdit()
        grid.addWidget(self.filename, 0, 1)
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 3, 0, -1, -1)
        self.setLayout(grid)

class MorphologyImageDialog(QDialog):

    def __init__(self,parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('Dilatation'), 0, 1)
        dilatation = QCheckBox()
        grid.addWidget(dilatation, 0, 0)
        grid.addWidget(QLabel('Opening'), 0, 3)
        opening = QCheckBox()
        grid.addWidget(opening, 0, 2)
        grid.addWidget(QLabel('Closing'), 0, 5)
        closing = QCheckBox()
        grid.addWidget(closing, 0, 4)
        grid.addWidget(QLabel('Erode'), 0, 7)
        erode = QCheckBox()
        grid.addWidget(erode, 0, 6)
        """dilatation.setChecked(True)"""
        choosesobel = QButtonGroup(self)
        choosesobel.addButton(dilatation)
        choosesobel.addButton(opening)
        choosesobel.addButton(closing)
        choosesobel.addButton(erode)
        if dilatation.isChecked():
            self.direction = 'dilatation'
        elif opening.isChecked():
            self.direction = 'opening'
        elif erode.isChecked():
            self.direction = 'erode'
        elif closing.isChecked():
            self.direction = 'closing'
        else:
            self.direction = 'none'
        self.show()
        box = QDialogButtonBox()
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.close)
        grid.addWidget(box, 10, 0, -1, -1)
        box.setWindowTitle("Morphology")
        self.setLayout(grid)