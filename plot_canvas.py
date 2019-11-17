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
        self.ax = self.fig.subplots(1, 1)
        self.ax.axis('off')
        self.axes = [self.ax]

    def render_image(self, ima):
        if ima.hist is None:
            self.ax = self.fig.subplots(1, 1)
            self.axes = [self.ax]
        else:
            self.ax = self.fig.subplots(1, 2)
            self.ax[1].plot(ima.hist[1][:], ima.hist[0][:], '-blue')
            twin_ax = self.ax[1].twinx()
            twin_ax.plot(ima.cdf[1][:], ima.cdf[0][:], '-red')
            self.axes = [self.ax[0], self.ax[1], twin_ax]
        if ima.noaxis:
            self.axes[0].axis('off')
        else:
            self.axes[0].axis('on')
        ima.render(self.axes[0])
        self.draw()
        
    def refresh(self):
        self.draw()

    def clear(self):
        for ax in self.axes:
            ax.clear()
            self.fig.delaxes(ax)
        self.draw()
 
