import sys, os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from plot_canvas import PlotCanvas
from vtkwidget import VTKWidget


class CentralWidget(QWidget):
    def __init__(self, scene, *args):
        super().__init__(*args)
        self.initUI(scene)

    def initUI(self, scene):
        self.layout = QHBoxLayout()
        self.visuwidget = PlotCanvas(self)
        self.layout.addWidget(self.visuwidget)
        self.vtkwidget = VTKWidget(scene, self)
        """sometimes we want to render with vtk, others we want to plot with plot canvas"""
        """so, if we want to render with vtk we hide the other and viceversa"""
        self.layout.addWidget(self.vtkwidget)
        self.vtkwidget.setHidden(True)
        self.setLayout(self.layout)

    def render_image(self, ima):
        if self.visuwidget.isHidden():
            self.visuwidget.setHidden(False)
            self.vtkwidget.setHidden(True)
        self.visuwidget.clear()
        self.visuwidget.render_image(ima)

    def render_surface(self, surf):
        if self.vtkwidget.isHidden():
            self.vtkwidget.setHidden(False)
            self.visuwidget.setHidden(True)
        self.vtkwidget.remove_all()
        self.vtkwidget.add_surface(surf)

    def render_volume(self, vol):
        if self.vtkwidget.isHidden():
            self.vtkwidget.setHidden(False)
            self.visuwidget.setHidden(True)
        self.vtkwidget.add_volume(vol)

