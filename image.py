from scipy import misc
from skimage import data
from scipy import misc
import numpy as np
import os


class Image:
    dic_procedural = {'coffee': data.coffee, 'astronaut': data.astronaut, 'ascent': misc.ascent, 'face': misc.face}

    def __init__(self, ima, title):
        self.title = title
        self.__ima = ima
        self.noaxis = True

    def __str__(self):
        return "Image: " + self.title

    def __getitem__(self, pos):
        i, j = pos
        return self.__ima[i][j]

    def __setitem__(self, pos, color):
        i, j = pos
        self.__ima[i][j] = color

    def size(self):
        i=0
        j=0
        while True:
            i +=1
            try:
                self.__ima[i][0]
            except:
                break
        while True:
            j += 1
            try:
                self.__ima[0][j]
            except:
                break
        return j, i

    def size_2(self):
        ima = self.__ima
        return ima.shape

    def nchannels(self):
        return self.__ima.shape[2]

    def render(self, ax):
        ax.imshow(self.__ima)

    def header(self, f):
        shape = self.size()
        shape = str(shape[0])+" "+str(shape[1])+" \n"
        header = "P3\n# This is a file by Gabriel Garcia.\n"+shape+"255\n"
        f.write(header)

    def save_ppm(self, filename):
        new_filename = filename + ".ppm"
        fd = open(new_filename, 'w')
        ima = self.__ima
        self.header(fd)
        ima.tofile(fd, sep=" ", format="%s")
        fd.close()

    def clip_circle(self, center, radius):
        radius2 = radius ** 2
        image = self.__ima
        n_channels = image.shape[2]
        alpha_channel = 255*np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8)
        alpha_image = np.dstack((image, alpha_channel))
        clipped_circle = np.zeros((2*radius, 2*radius, 4), dtype=np.uint8)
        for i in range(radius * 2):
            for j in range(radius * 2):
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius2:
                    clipped_circle[i, j] = alpha_image[(center[0]+i-radius), (center[1]+j-radius)]
                else:
                    clipped_circle[i, j] = (0, 0, 0, 0)
        clipped_circle = Image.convert_numpy_to_image(clipped_circle, 'clipped circle')
        return clipped_circle

    @classmethod
    def convert_numpy_to_image(cls, image, title):
        ima = np.zeros((image.shape[0], image.shape[1], image.shape[2]), dtype=np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                ima[i, j] = image[i, j]
        return cls(image, title)

    @classmethod
    def read_file(cls, filename):
        ima = np.loadtxt(filename, dtype=np.uint8)
        return cls(ima, filename)

    @classmethod
    def create_procedural(cls, name):
        ima = cls.dic_procedural[name]()
        return cls(ima, name)

    @classmethod
    def create_uniform(cls, width, height, color):
        nchannels = len(color)
        ima = np.zeros((height, width, nchannels), dtype=np.uint8)
        ima[:, :] = color
        return cls(ima, 'Uniform')

    @classmethod
    def create_circle(cls, radius, color):
        radius2 = radius ** 2
        ima = np.zeros((radius * 2, radius * 2, 4), dtype=np.uint8)
        for i in range(radius * 2):
            for j in range(radius * 2):
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius2:
                    ima[i, j] = color
                else:
                    ima[i, j] = (0, 0, 0, 0)
        return cls(ima, 'circle')
