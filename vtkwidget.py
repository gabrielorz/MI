"""
Module vtkwidget
Author: Dani Tost - CREB

It defines the widget that support DVR and IVR of all objects of a scene
"""


import vtk
from PyQt5 import QtWidgets, QtGui
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class VTKWidget(QVTKRenderWindowInteractor) :
    
    def __init__(self, scene, parent = None):
        super().__init__(parent)
        self.scene = scene
        self.initUI()

    def initUI(self):
        self.render_window = self.GetRenderWindow()
        self.interactor = self.render_window.GetInteractor()
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground((0.80, 0.85, 0.75))
        self.render_window.AddRenderer(self.renderer)
        self.interactor.Initialize()
        self.interactor.Start()
        self.show()

    def remove_all(self):
        self.renderer.RemoveAllViewProps()

    def add_volume(self, volume):
        self.remove_all()
        self.renderer.AddVolume(volume)
        self.refresh()
        
    def add_surface(self, surface):
        self.renderer.AddActor(surface)
        self.refresh()

    def refresh(self):
        self.renderer.ResetCamera()
        self.render_window.Render()

        
    def close(self):
        self.remove_all()
        self.refresh()
