#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:10:23 2019

@author: gabriel.garcia.hernando
"""
import vtk

class Volume(vtk.vtkVolume):
    def __init__(self,name,source,mat):
        super().__init__()
        self.name = name
        mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        mapper.SetBlendModeToComposite()
        self.SetMapper(mapper)
        self.SetProperty(mat)

    @classmethod
    def from_VTK_file(cls, filename, mat):
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(filename)
        return cls('file', reader, mat)