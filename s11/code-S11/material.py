import vtk
class SurfaceMaterial(vtk.vtkProperty) :
    def __init__(self, name, Od, kd, Os, ks, n, alpha) :
        super().__init__()
        self.name = name
        self.SetDiffuseColor(Od[0], Od[1], Od[2])
        self.SetDiffuse(kd) 
        self.SetSpecularColor(Os[0], Os[1], Os[2])
        self.SetSpecular(ks) 
        self.SetSpecularPower(n) 
        self.SetOpacity(alpha)
        #self.SetBackfaceCulling(True)
        
    @classmethod
    def default(cls):
        return cls('default', (1, 0, 1), 0.7, (1, 1, 1), 0.3, 50, 1)


class VolumeMaterial(vtk.vtkVolumeProperty) :
    def __init__(self, name, rgb, opac, kd, ks, n):
        self.name = name
        colorTF = vtk.vtkColorTransferFunction()
        for point in rgb :
            colorTF.AddRGBPoint(point[0], point[1][0], point[1][1] , point[1][2])
        self.SetColor(colorTF)
        opacTF = vtk.vtkPiecewiseFunction()
        for point in opac :
            opacTF.AddPoint(point[0], point[1])
        self.SetScalarOpacity(opacTF)

    
        self.SetInterpolationTypeToLinear()

        self.SetDiffuse(kd)
        self.SetSpecular(ks)
        self.SetSpecularPower(n)
        self.ShadeOn()
        """"add set of predefined materials and create new material either for surface or volume, you should be able to change the material of the volume or the surface """
        """ define transfer function for volume segmentation"""
        """ask about the volume, resolution, faces"""
        """ save the file """
        """ optional, dicom read"""
    @classmethod
    def default(cls):
        opac = ((0, 0), (255, 1))
        rgb = ((0, (0, 0, 0)), (255, (1, 1, 1)))
        return cls('default', rgb, opac, 0.5, 0.3, 50)
