from scipy import misc
from skimage import data
from scipy import misc
import numpy as np
from PIL import Image as IMG
import os
import io


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
        ima = self.__ima
        i = ima.shape[0]
        j = ima.shape[1]
        return j, i

    def size_2(self):
        ima = self.__ima
        return ima.shape

    def nchannels(self):
        length = self.__ima
        dimensions = length.shape
        if len(dimensions) == 2:
            channels = 1
        else:
            channels = dimensions[2]
        return channels

    def render(self, ax):
        ax.imshow(self.__ima)
        ax.title.set_text(self.title)
        ax.axis('off')

    def header_ppm(self, f):
        shape = self.size()
        shape = str(shape[0]) + " " + str(shape[1]) + " \n"
        header = "P3\n# This is a file by Gabriel Garcia.\n" + shape + "255\n"
        f.write(header)

    def save_ppm(self, filename):
        new_filename = filename
        fd = open(new_filename, 'w')
        ima = self.__ima
        self.header_ppm(fd)
        ima.tofile(fd, sep=" ", format="%s")
        fd.close()

    def clip_circle(self, center, radius):
        radius2 = radius ** 2
        alpha_image = self.add_alpha_channel(255)
        clipped_circle = np.zeros((2*radius, 2*radius, alpha_image.shape[2]), dtype=np.uint8)
        i_max = alpha_image.shape[0]
        j_max = alpha_image.shape[1]
        zero_color = np.zeros(alpha_image.shape[2], dtype=np.uint8)
        for i in range(radius * 2):
            for j in range(radius * 2):
                pos1 = center[0] + i - radius
                pos2 = center[1] + j - radius
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius2 and i < i_max and j < j_max and pos1 > 0 and pos2 > 0:
                    clipped_circle[i, j] = alpha_image[pos1, pos2]
                    clipped_circle[i, j][3] = 255
                else:
                    clipped_circle[i, j] = zero_color
        clipped_circle = Image.convert_numpy_to_image(clipped_circle, 'clipped circle')
        return clipped_circle

    def transform_image_to_numpy(self):
        image = self.__ima
        size = self.size()
        i_max = size[0]
        j_max = size[1]
        n_channels = self.nchannels()
        numpy_image = np.zeros((j_max, i_max, n_channels), dtype=np.uint8)
        for i in range(i_max):
            for j in range(j_max):
                numpy_image[j, i] = image[j, i]
        return numpy_image

    def add_alpha_channel(self, value):
        image = self.__ima
        n_channels = self.nchannels()
        alpha_channel = value * np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8)
        if n_channels == 2 or n_channels == 4:
            alpha_image = image
        elif n_channels == 1 or n_channels == 3:
            alpha_image = np.dstack((image, alpha_channel))
        else:
            return print('what is this image dude')
        return alpha_image

    def clip_circle_smart(self, center, radius):
        img = self.add_alpha_channel(255)
        mask = self.create_circular_mask(center, radius)
        masked_img = img.copy()
        masked_img[~mask] = 0
        w, h = 0, 0
        for i in range (masked_img.shape[0]):
            for j in range(masked_img.shape[1]):
                if mask[i, j] and j >= w and j >=i:
                    w = j
                if mask[i, j] and i >= h and i >= j:
                    h = i
        cropped_masked_img = np.zeros((h, w, masked_img.shape[2]), dtype=np.uint8)
        cropped_masked_img[:, :] = masked_img[0:h, 0:w]
        cropped = Image.convert_numpy_to_image(cropped_masked_img, 'clipped_circle_smart'+'_'+self.title)
        return cropped

    def create_circular_mask(self, center=None, radius=None):
        size = self.size()
        h = size[1]
        w = size[0]
        if center is None:  # use the middle of the image
            center = [int(w / 2), int(h / 2)]
        if radius is None:  # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w - center[0], h - center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = dist_from_center <= radius
        return mask

    @classmethod
    def convert_numpy_to_image(cls, image, title):
        ima = np.zeros((image.shape[0], image.shape[1], len(image[0, 0])), dtype=np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                ima[i, j] = image[i, j]
        return cls(image, title)

    @classmethod
    def read_file(cls, filename):
        image_string = open(filename, 'rb').read()
        image = IMG.open(io.BytesIO(image_string))
        arr = np.asarray(image)
        name = os.path.splitext(filename)[0]
        path = name.rstrip(os.sep)
        name = os.path.basename(path)
        return cls(arr, name)

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
