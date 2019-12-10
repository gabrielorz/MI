"""
An example of widget that plots things: it can be an image or whatever
Render the curves on top of the image
Render the histogram (in a separate subplot)

MUEI- Medical Images
Dani Tost- 2019
"""
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor 

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None): 
        self.fig = Figure()
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.axis('off')
        self.naxes = 1
        
    def render_image(self, ima) :
        self.ax = self.fig.add_subplot(1, 1, 1)
        ima.render(self.ax, self.naxes)
        self.draw()
        
    def refresh(self):
        self.draw()

    def clear(self) :
        if self.naxes == 1:
            self.ax.remove()
        else:
            for ax in self.ax:
                ax.remove()
