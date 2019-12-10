import json
from box import Box2D    
from polygon import Polygon

class PolygonList:
    def __init__(self, polygons):
        self.polygons = polygons
        self.box = self.bounding_box()
        
    def __str__(self) :
        return 'List of {:} polygons'.format(len(self))
    
    def __len__(self) :
        return len(self.polygons)

    def __getitem__(self, i) :
        return self.polygons[i]

    def bounding_box(self) :
        if len(self) > 0:
            bb = self[0].bounding_box()
            for i in range(1, len(self)):
                bb2 = self[i].bounding_box()
                if bb2.xmin < bb.xmin:
                    bb.xmin =  bb2.xmin
                if bb2.ymin < bb.ymin:
                    bb.ymin =  bb2.ymin
                if bb2.xmax > bb.xmax:
                    bb.xmax =  bb2.xmax
                if bb2.ymax > bb.ymax:
                    bb.ymax =  bb2.ymax
            return bb
        else:
            return Box2D(0, 0, 1, 1)

    @classmethod        
    def __decoder__(cls, dic):
        if  "__type__" in dic and dic["__type__"] =="polygon":
            return (Polygon(dic['color'], dic['vertices']))
        else:
            raise IOError("Not a valid file format")

        
    @classmethod
    def  FromJson(cls, filename) :
        with open(filename, 'r') as f:
            polygons = json.load(f, object_hook=cls.__decoder__)
            return cls(polygons)
        return cls(None)
        
