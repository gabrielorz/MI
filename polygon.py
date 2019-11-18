import json
import numpy as np
from box import Box2D
class Polygon:
    def __init__(self, color, vertices):
        self.vert= vertices
        self.color = color

    def __len__(self) :
        return len(self.vert)

    def __getitem__(self, i) :
        return self.vert[i]
    
    def __str__(self) :
        return 'Polygon of {:} vertices'.format(len(self))

    def  bounding_box(self) :
        """
        Returns the smallest bounding box of the polygon
        """
        if len(self) > 0:
            xmin, ymin = self.vert[0]
            xmax, ymax = self.vert[0]
            for i in range(1, len(self)):
                if self[i][0] < xmin:
                    xmin = self[i][0]
                if self[i][1] < ymin:
                    ymin = self[i][1]
                if self[i][0] > xmax:
                    xmax = self[i][0]
                if self[i][1] > ymax:
                    ymax = self[i][1]                                        
            return Box2D(xmin, ymin, xmax, ymax)
        else:
            return Box2D(0, 0, 1, 1)

    def rasterize(self, tr):
        """
        Returns the list of rasterized vertices
        given a rasterization transformation matrix (sx, sy, tx, ty)
        """
        x = []
        y = []
        for v in self :
            x.append(int(v[0]*tr[0] +tr[2]))
            y.append(int(v[1]*tr[1] +tr[3]))
        return np.asarray(x), np.asarray(y)

