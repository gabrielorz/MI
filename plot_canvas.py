"""
An example of widget that plots things: it can be an image or whatever
Render the curves on top of the image
Render the histogram (in a separate subplot)

MUEI- Medical Images
Dani Tost- 2018
"""
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=12, height=12,  dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.axis('off')
        self.axes = []

    def render_image(self, ima):
        if ima.noaxis:
            self.ax.axis('off')
        else:
            self.ax.axis('on')
        ima.render(self.ax)
        self.draw()
        
    def refresh(self):
        self.draw()

    def clear(self, i) :
        self.ax.clear()
        self.draw()
 
