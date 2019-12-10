from scipy import misc
from skimage import data
from skimage import draw
from skimage import exposure, color
from  scipy import misc
import numpy as np
import os
import os


class Image:
    dic_procedural = {'coffee': data.coffee, 'astronaut': data.astronaut, 'ascent':misc.ascent, 'face': misc.face, 'checkerboard':data.checkerboard, 'horse':data.horse, 'coins': data.coins}
    def __init__(self, ima, title) :
        self.name = title
        self.__ima = ima
        self.noaxis = True
        
    def __str__(self) :
        return "Image: " + self.name

    def __getitem__(self, pos) :
        i, j = pos
        return self.__ima[i][j]

    def __setitem__(self, pos, color) :
        i, j = pos
        self.__ima[i][j] = color

        
    def size(self) :
        return self.__ima.shape[1], self.__ima.shape[0]

    def nchannels(self) :
        if len(self.__ima.shape) == 3 :
            return self.__ima.shape[2]
        else:
            return 1

    def render_values(self, ax):
        ax.set_title(self.name)
        ax.imshow(self.__ima)
        if self.noaxis :
            ax.axis('off')

    def render(self, ax, naxis) :
        if naxis == 1:
            self.render_values(ax)
        else:
            self.render_values(ax[0])
            
    @classmethod
    def read_file(cls, filename):
        ima = misc.imread(filename)
        name_w_ext = os.path.basename(filename)
        name, extension = os.path.splitext(name_w_ext)
        return cls(ima, name)

    @classmethod
    def create_procedural(cls, name):
        ima = cls.dic_procedural[name]()
        return cls(ima, name)
