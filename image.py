from scipy import misc
from skimage import data
from  scipy import misc
import numpy as np
import os

class Image:
    dic_procedural = {'coffee': data.coffee, 'astronaut': data.astronaut, 'ascent':misc.ascent, 'face': misc.face}
    def __init__(self, ima, title) :
        self.title = title
        self.__ima = ima
        self.noaxis = True

    def __str__(self) :
        return "Image: " + self.title

    def __getitem__(self, pos) :
        i, j = pos
        return self.__ima[i][j]

    def __setitem__(self, pos, color) :
        i, j = pos
        self.__ima[i][j] = color

    def size(self) :
        pass

    def nchannels(self) :
        pass

    def render(self, ax) :
        ax.imshow(self.__ima)
    
    def save_ppm(self, filename):
        pass
    
    def clip_circle(self, center, radius):
        pass

    @classmethod
    def read_file(cls, filename):
        "next week"
        pass

    @classmethod
    def create_procedural(cls, name):
        ima = cls.dic_prodcedural[name]()
        "next week"

    @classmethod
    def create_uniform(cls, width, height, color) :
        nchannels = len(color)
        ima = np.zeros((height, width, nchannels), dtype=np.uint8)
        ima[:, :]=color
        return cls(ima, 'uniform')
    @classmethod
    def create_circle(cls,radius,color) :
        nchannels = 4
        radius2=radius**2
        ima=np.zeros((radius*2,radius*2,nchannels),dtype = np.uint8)
        for i in range(radius*2):
            for j in range(radius*2):
                if (i-radius)**2 + (j-radius)**2<=radius2:
                    ima[i,j]=color
                else:
                    ima[i,j]=(0,0,0,0)
        return cls(ima, 'circle')
