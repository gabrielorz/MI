#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:32:12 2019

@author: gabriel.garcia.hernando
"""
import vtk

class SurfaceMaterial(vtk.vtkProperty):
    def __init__(self, name, Od, kd, Os, ks, n, alpha):
        super().__init__()
        self.name = name
        self.SetDiffuseColor(Od[0],Od[1],Od[2])
        self.SetDiffuse(kd)
        self.SetSpecularColor(Os[0],Os[1],Os[2])
        self.SetSpecular(ks)
        self.SetSpecularPower(n)
        self.SetOpacity(alpha)
        
class VolumeMaterial(vtk.vtkVolumeProperty) :
    def __init__(self, name, rgb, opac=None, grad=None, interpol='nearest', shade = False):
        self.name = name
        colorTF = vtk.vtkColorTransferFunction()
        for point in rgb :
            colorTF.AddRGBPoint(point[0], point[1][0], point[1][1] , point[1][2])
        self.SetColor(colorTF)
        opacTF = vtk.vtkPiecewiseFunction()
        for point in opac :
            opacTF.AddPoint(point[0], point[1])
            self.SetScalarOpacity(opacTF)