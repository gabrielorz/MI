""" AUTHOR: GABRIEL GARCIA """

import matplotlib.pyplot as plt
from image import Image
from imagelist import ImageList


def create_fig(nrows, ncols):
    fig, ax = plt.subplots(nrows, ncols)
    fig.canvas.set_window_title("IM2019- Lab1")
    text = fig.suptitle('Created images', fontsize=20)
    return fig, ax


def image_configuration(nplots):
    rows = 1
    cols = 1
    while rows*cols < nplots:
        if cols <= rows:
            cols = cols + 1
        else:
            rows = rows + 1
    return rows, cols


if __name__ == '__main__':

    width, height = 500, 300
    color = (255, 255, 0)
    images = ImageList()
    images.append(Image.create_uniform(width, height, (255, 255, 0)))
    images.append(Image.create_procedural('coffee'))
    images.append(Image.create_procedural('face'))
    images.append(Image.create_procedural('astronaut'))
    images.append(Image.create_procedural('ascent'))
    images.append(Image.read_file('./resources/images/spect.png'))
    images.append(Image.create_procedural('camera'))
    images.append(Image.create_procedural('checkerboard'))
    images.append(Image.create_procedural('clock'))
    images.append(Image.create_procedural('coins'))
    images.append(Image.create_procedural('horse'))
    images.append(Image.read_file('./resources/images/brain.jpg'))
    images.append(Image.read_file('./resources/images/spect.png'))
    ima = Image.create_procedural('face')
    clip_face = ima.clip_circle((300,650),250)
    clip_face.save_ppm('./resources/images/clip_face.pnm')
    images.append(clip_face)
    nrows, ncols = image_configuration(len(images))
    fig, ax = create_fig(nrows, ncols)
    images.render(ax)
    plt.show()

