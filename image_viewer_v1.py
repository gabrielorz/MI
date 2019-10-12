import matplotlib.pyplot as plt
from image import Image


def create_fig(nrows, ncols):
    fig, ax = plt.subplots(nrows, ncols)
    fig.canvas.set_window_title("IM2019- Lab1")
    text = fig.suptitle('Created images', fontsize=20)
    return fig, ax


def image_configuration(nplots):
    return 1, 1


if __name__=='__main__':
    width, height = 500, 400
    ima = Image.create_uniform(width, height, (255, 255, 0))
    ima.save_ppm('../resources/images/prova')
    nrows, ncols = image_configuration(1)
    fig, ax = create_fig(nrows, ncols)
    ima.render(ax)
    plt.show()


