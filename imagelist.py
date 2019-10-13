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
    
    def append(self, ima):
        self.__images.append(ima)
    
    def render(self, ax):
        nrows = ax.shape[0]
        ncols = ax.shape[1]
        n = 0
        for row in range(nrows):
            for col in range(ncols):
                ax[row, col].imshow(self[n])
                ax[row, col].title.set_text(self[n].title)
                ax[row, col].axis('off')
                n = n + 1
                if n > len(self) - 1:
                    break
