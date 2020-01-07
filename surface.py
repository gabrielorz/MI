import vtk
import os
from paramdialog import SaveSTLDialog

class Surface(vtk.vtkActor) :
    def __init__(self, name, source,  mat=None):
        super().__init__()
        self.name = name
        self.source = source
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
        if mat is not None:
            self.SetProperty(mat)

    @classmethod
    def from_sphere(cls, center, radius, res, mat=None):
        source = vtk.vtkSphereSource()
        source.SetCenter(center)
        source.SetRadius(radius)
        source.SetThetaResolution(res[0])
        source.SetPhiResolution(res[1])
        return cls('sphere', source, mat)


    @classmethod
    def read_file(cls, filename, mat=None):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        base_name = os.path.basename(filename)
        name, extension = os.path.splitext(base_name)
        surf = cls(name, reader, mat)
        return surf


    @classmethod
    def from_volume(cls, vol, values, mat):
        source = vtk.vtkMarchingCubes() 
        source.SetValue(values[0], values[1])
        source.SetInputConnection(vol.reader.GetOutputPort())
        name = vol.name +'-{}-{}'.format(values[0], values[1])
        return cls(name, source, mat)
    
    @classmethod
    def from_mobius(cls, mat=None):
        mobius = vtk.vtkParametricMobius()
        mobius.SetRadius(2)
        mobius.SetMinimumV(-0.5)
        mobius.SetMaximumV(0.5)
        source = vtk.vtkParametricFunctionSource()
        source.SetParametricFunction(mobius)
        return cls('mobius', source, mat)

    @classmethod
    def from_boy(cls, mat=None):
        boy = vtk.vtkParametricBoy()
        source = vtk.vtkParametricFunctionSource()
        source.SetParametricFunction(boy)
        return cls('boy', source, mat)

    @classmethod
    def from_conicspiral(cls, mat=None):
        conicspiral = vtk.vtkParametricConicSpiral()
        source = vtk.vtkParametricFunctionSource()
        source.SetParametricFunction(conicspiral)
        return cls('conicspiral', source, mat)

    @classmethod
    def from_crosscap(cls, mat=None):
        crosscap = vtk.vtkParametricCrossCap()
        source = vtk.vtkParametricFunctionSource()
        source.SetParametricFunction(crosscap)
        return cls('crosscap', source, mat)
    
    @classmethod
    def from_STL_file(cls, filename, mat=None):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        return cls('file', reader, mat)


    def to_stl(self):
        writer = vtk.vtkSTLWriter()
        param = SaveSTLDialog(self)
        if param.exec_():
            filename = param.filename
        else:
            filename = 'unnamed'
        writer.SetInputConnection(self.cur_surface.source.GetOutputPort())
        """writer.SetFileTypeToBinary()"""
        writer.SetFileName(filename + '.stl')
        writer.Write()