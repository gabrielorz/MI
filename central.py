import sys, os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from plot_canvas import PlotCanvas

class CentralWidget(QWidget) :
    def __init__(self, *args):
        super().__init__(*args)
        self.initUI()
        
    def initUI(self):
        self.layout=  QVBoxLayout()
        self.visuwidget = PlotCanvas(self)
        self.layout.addWidget(self.visuwidget)
        self.setLayout(self.layout)
        
    def render_image(self, ima):
        self.visuwidget.render_image(ima)
