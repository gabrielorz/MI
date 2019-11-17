""" AUTHOR: GABRIEL GARCIA """
"""
A class containing a list of images

"""


class ImageList:

    def __init__(self):
        self.__images = []

    def __getitem__(self, i):
        return self.__images[i]

    def __setitem__(self, i, ima):
        self.__images[i] = ima

    def __len__(self):
        return len(self.__images)

    def __str__(self):
        return "List of {:} images".format(len(self))

    def index(self, name):
        return self.__images.index(name)
    
    def append(self, ima):
        self.__images.append(ima)
    
    def render(self, ax):
        if len(self.__images) == 1:
            self.__images[0].render(ax)
            return
        nrows = ax.shape[0]
        ncols = ax.shape[1]
        n = 0
        for row in range(nrows):
            for col in range(ncols):
                if n <= len(self) - 1:
                    self.__images[n].render(ax[row, col])
                    n = n + 1
                else:
                    ax[row, col].set_axis_off()