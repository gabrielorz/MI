import vtk
from surface import Surface
from material import SurfaceMaterial, VolumeMaterial
from volume import Volume

class Rendering :
    def __init__(self, size, color) :
        
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(color[0], color[1], color[2])
        self.window = vtk.vtkRenderWindow()
        self.window.SetSize(size[0], size[1])
        self.window.AddRenderer(self.renderer)
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)

def main() :
    ren = Rendering((200, 300), (1, 0, 0))
    mat_sphere = SurfaceMaterial('orange_wall',(1, 0.7, 0.0), 0.8, (1,1,1), 0, 50, 1.0)
    asphere = Surface.from_sphere((0,0,0,),1,(1,31),mat_sphere)
    
    mat_mobius = SurfaceMaterial('pink_metallic',(1, 0.8, 1), 0.1, (1,1,1), 0.9, 50, 1.0)
    amobius = Surface.from_mobius(mat_mobius)
    
    liver = Surface.from_STL_file('liver.stl')
    
    mat_head = VolumeMaterial('head',[(0,(0,0,0)),(1000,(1,1,1))],[(0,0), (500,0), (4000,1)])
    head = Volume.from_VTK_file('head.vtk', mat_head)
    
    ren.renderer.AddVolume(head)
    ren.renderer.AddActor(liver)
    ren.renderer.AddActor(asphere)
    ren.renderer.AddActor(amobius)
    ren.interactor.Initialize()
    ren.interactor.Start()
	

if __name__ == '__main__':
    main()

