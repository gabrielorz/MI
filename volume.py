#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:10:23 2019

@author: gabriel.garcia.hernando
"""

import vtk
import numpy as np
from os.path import basename, splitext
from material import VolumeMaterial


class Volume(vtk.vtkVolume):
    def __init__(self, name, reader, res, spacing, mat):
        self.name = name
        mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetBlendModeToComposite()
        self.SetMapper(mapper)
        self.SetProperty(mat)
        self.reader = reader
        self.res = res
        self.spacing = spacing

    def extractSurface(self, vmin, vmax):
        mc = vtk.vtkMarchingCubes()
        mc.SetInput(self.data.GetOutput())
        mc.SetValue(vmin, vmax)
        return mc

    @classmethod
    def read_file(cls, filename, mat=None):
        name, ext = splitext(basename(filename))
        if ext[1:] != 'vtk':
            return None
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(filename)
        reader.Update()
        try:
            reader_output = reader.GetOutput()
            minv, maxv = reader_output.GetScalarRange()
            res = reader_output.GetDimensions()
            spacing = reader_output.GetSpacing()
        except:
            return None
        if mat == None:
            mat = VolumeMaterial.uniform(name, minv, maxv, min(res))
        return cls(name, reader, res, spacing, mat)

    @classmethod
    def from_VTK_file(cls, filename, mat=None):
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(filename)
        reader.Update()
        return cls('file', reader, mat)

