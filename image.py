""" AUTHOR: GABRIEL GARCIA & ARNAU PERA"""

from scipy import misc
from skimage import data
from skimage import color
from skimage import exposure
from skimage import filters, restoration, measure, morphology
from skimage.util import random_noise
from scipy import misc
import numpy as np
from PIL import Image as IMG
import os
import io
import matplotlib.pyplot as plt


class Image:
    dic_procedural = {'coffee': data.coffee, 'astronaut': data.astronaut, 'ascent': misc.ascent, 'face': misc.face, 'camera': data.camera,  'checkerboard': data.checkerboard, 'clock': data.clock, 'coins': data.coins,  'horse': data.horse}

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

    def create_histogram(self):
        im = self.__ima
        gray = color.rgb2gray(im)
        y, x = exposure.histogram(gray)
        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(im)
        ax[1].plot(x,y)
        ax[0].title.set_text(self.title)
        ax[0].axis('off')
        ax[1].axis('off')
        ax[1].title.set_text('Histogram')
        plt.show()

    def nchannels(self):
        length = self.__ima
        dimensions = length.shape
        if len(dimensions) == 2:
            channels = 1
        else:
            channels = dimensions[2]
        return channels

    def render(self, ax):
        if self.nchannels() == 1:
            ax.imshow(self.__ima, cmap='gray')
        else:
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
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius2 and i < i_max and j < j_max and i_max > pos1 > 0 and j_max > pos2 > 0:
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
        for i in range(masked_img.shape[0]):
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
    
    def gaussian(self, sigma):
        array_np = filters.gaussian(self.__ima, sigma, multichannel=False)
        title = self.title+'_gaussian_sigma='+str(sigma)
        return Image(array_np, title)

    def billateral(self):
        array_np = restoration.denoise_bilateral(self.__ima, multichannel=True)
        title = self.title+'_billateral'
        return Image(array_np, title)

    def chambolle(self, weight, epsilon):
        array_np = restoration.denoise_tv_chambolle(self.__ima, weight, epsilon)
        title = self.title+'_chambolle_weight='+str(weight)+'_epsilon='+str(epsilon)
        return Image(array_np, title)

    def wavelet(self):
        array_np = restoration.denoise_wavelet(self.__ima)
        title = self.title+'_wavelet'
        return Image(array_np, title)

    def add_noise(self, sigma):
        array_np = random_noise(self.__ima, var = sigma**2)
        title = self.title+'_noisy'
        return Image(array_np, title)

    def user_threshold(self, threshold):
        array_np = color.rgb2gray(self.__ima)
        array_np = array_np > threshold/255
        title = self.title+'_user_threshold'
        return Image(array_np, title)

    def otsu_threshold(self):
        array_np = color.rgb2gray(self.__ima)
        t_otsu = filters.threshold_otsu(array_np)
        array_np = array_np > t_otsu
        title = self.title+'_otsu_threshold'
        return Image(array_np, title)

    @classmethod
    def call_proc_dict(cls):
        return cls.dic_procedural.keys()

    def sobel_filter(self, direction):
        array_np = color.rgb2gray(self.__ima)
        if direction == 'both':
            array_np = filters.sobel(array_np)
            title = self.title + '_sobel'
        elif direction == 'horizontal':
            array_np = filters.sobel_h(array_np)
            title = self.title + 'sobel_h'
        elif direction == 'vertical':
            array_np = filters.sobel_v(array_np)
            title = self.title+'_sobel_v'
        else:
            title = self.title
        return Image(array_np, title)

    def find_contours(self, threshold=0.8):
        array_np = color.rgb2gray(self.__ima)
        contours = measure.find_contours(array_np, threshold)
        title = self.title+'_contours'
        array_np = array_np + contours
        return Image(array_np, title)

    def contrast_stretch(self, pmin, pmax):
        array_np = self.__ima
        p1, p2 = np.percentile(array_np, (pmin, pmax))
        array_np = exposure.rescale_intensity(array_np, in_range=(p1, p2))
        title = self.title+'_contrasted_'+str(pmin)+'-'+str(pmax)
        return Image(array_np, title)

    def morphology(self, direction):
        array_np = color.rgb2gray(self.__ima)
        if direction == 'dilatation':
            array_np = morphology.dilation(array_np)
            title = self.title + '_dilatation'
        elif direction == 'open':
            array_np = morphology.opening(array_np)
            title = self.title + '_opening'
        elif direction == 'closing':
            array_np = morphology.closing(array_np)
            title = self.title+'_closing'
        elif direction == 'erode':
            array_np = morphology.erosion(array_np)
            title = self.title+'_erode'
        else:
            title = self.title
        return Image(array_np, title)
