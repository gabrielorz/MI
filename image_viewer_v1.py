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
    color = (255,255, 0)
    images = ImageList()
    images.append(Image.create_uniform(width, height, (255, 255, 0)))
    images.append(Image.create_procedural('coffee'))
    images.append(Image.create_procedural('face'))
    images.append(Image.create_procedural('astronaut'))
    images.append(Image.create_procedural('ascent'))
    """ima.save_ppm('../resources/images/prova')"""
    nrows, ncols = image_configuration(len(images))
    fig, ax = create_fig(nrows, ncols)
    n = 0
    for row in range(nrows):
        for col in range(ncols):
            images[n].render(ax[row, col])
            ax[row, col].title.set_text(images[n].title)
            ax[row, col].axis('off')
            n = n+1
            if n >= len(images):
                break
    plt.show()

