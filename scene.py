from objectlist import ObjectList, ImageList
from material import SurfaceMaterial, VolumeMaterial
class Scene:
    def __init__(self) :
        self.images = ImageList()
        self.cur_image = None
        self.surfaces = ObjectList()
        self.cur_surface = None
        self.volumes = ObjectList()
        self.cur_volume = None
        self.materials = {'surface_default': SurfaceMaterial.default(), 'bronze': SurfaceMaterial.bronze(), 'silver': SurfaceMaterial.silver(), 'gold': SurfaceMaterial.gold(), 'volume_default': VolumeMaterial.default()}
        
    def material(self, name='surface_default'):
        return self.materials[name]

