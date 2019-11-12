"""
MUEI- ETSEIB
Medical images- Cur 2019-20-Q1
Dani Tost

Preliminary version of the interface
"""
import sys

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QAction, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon

from central import CentralWidget
from imagelist import ImageList
from image import Image
from paramdialog import *
from polygonlist import PolygonList
from skimage import filters

class MainWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.images = ImageList()
        self.cur_image= None   # The one visible 
        self.initUI()
        
    def initUI(self):
        self.create_menus()
        self.central = CentralWidget()
        self.setCentralWidget(self.central)
        self.show()
        
    def create_menus(self) :
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.create_file_menu()
        self.create_image_menu()
        self.create_tools_menu()
        self.create_selection_menu()
        self.create_filter_menu()
        self.create_help_menu()


    def create_filter_menu(self):
        "Menu Filter"
        self.menuFilter = self.menubar.addMenu('Filter')
        "Submenu Denoising"
        "Action Gaussian blurring"
        self.menuDenoising = self.menuFilter.addMenu('Denoising')
        gaussianAction = QAction(QIcon('gaussian.png'),'Gaussian', self)
        gaussianAction.triggered.connect(self.gaussian_filter)
        self.menuDenoising.addAction(gaussianAction)
        "Submenu Contouring"
        "Action contouring"
        self.menuContouring = self.menuFilter.addMenu('Countouring')
        contouringAction = QAction(QIcon('contouring.png'),'Contour algorithm name', self)
        contouringAction.triggered.connect(self.countouring)
        self.menuContouring.addAction(contouringAction)
        "Submenu Segmentation"
        self.menuSegmentation = self.menuFilter.addMenu('Segmentation')
        "Action segmentation"
        segmentationAction = QAction(QIcon('segmentation.png'),'Segmentation algorithm name', self)
        segmentationAction.triggered.connect(self.segmentation)
        self.menuSegmentation.addAction(segmentationAction)

        
    def create_selection_menu(self):
        self.menuSelection = self.menubar.addMenu('Selection')
        for i in range(len(self.images)):
            im = self.images[i]
            selectImageAction = QAction(im.title, self)  
            selectImageAction.triggered.connect(self.select_image(im.title)) 
            self.menuSelection.addAction(selectImageAction)
            
       
    def create_file_menu(self):
        self.menuFile = self.menubar.addMenu('File')

        readImageAction = QAction(QIcon('read.png'), 'Read image', self)
        readImageAction.setShortcut('Ctrl+F')
        readImageAction.triggered.connect(self.read_image)
        self.menuFile.addAction(readImageAction)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.menuFile.addAction(exitAction)

    def create_tools_menu(self):
        self.menuTools = self.menubar.addMenu('Tools')

        self.menuCreateHistogram = self.menuTools.addMenu('Create Histogram')
        histogramAction = QAction(QIcon('resources/icons.png'), 'Uniform', self)
        histogramAction.triggered.connect(self.create_histogram)
        self.menuImage.addAction(histogramAction)

    def create_image_menu(self):
        self.menuImage = self.menubar.addMenu('Images')
        self.menuProcedural = self.menuImage.addMenu('Procedural')
        proceduralAction = QAction('Procedural', self)
        faceAction = QAction(QIcon('gaussian.png'),'face', self)
        faceAction.triggered.connect(self.procedural_image)
        self.menuProcedural.addAction(faceAction)
        coffeeAction = QAction(QIcon('gaussian.png'),'coffee', self)
        coffeeAction.triggered.connect(self.procedural_image)
        self.menuProcedural.addAction(coffeeAction)
        proceduralAction.triggered.connect(self.procedural_image)
        uniformAction = QAction(QIcon('resources/icons.png'), 'Uniform', self)  
        uniformAction.setShortcut('Ctrl+H')
        uniformAction.triggered.connect(self.uniform_image)
        self.menuImage.addAction(uniformAction)
        rasterizeAction = QAction(QIcon('resources/icons.png'), 'Rasterization', self)
        rasterizeAction.triggered.connect(self.rasterize_image)
        self.menuImage.addAction(rasterizeAction)


    def create_help_menu(self):
        "Menu Help"
        self.menuHelp = self.menubar.addMenu('Help')
        "Action Help"
        helpAction = QAction(QIcon('resources/icons.png'), 'Help', self)  
        helpAction.setShortcut('Ctrl+H')
        helpAction.triggered.connect(self.help_action)
        self.menuHelp.addAction(helpAction)
        "Action About"
        aboutAction = QAction(QIcon('icons/about.png'), 'About', self)
        aboutAction.triggered.connect(self.about)
        self.menuHelp.addAction(aboutAction)

        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure to exit?", QMessageBox.Yes | 
                                           QMessageBox.No, QMessageBox.No)
         
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()           

    def help_action(self) :
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
        
    def about(self) :
        text = 'Image viewer by Gabriel García'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()

    def read_image(self) :
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self,"Read image file", "","", options=options)
        if ok:
            im = Image.read_file(filename)
            self.add_image(im)

    def get_basic_params(self):
        param = ParamImageDialog(self)
        if param.exec_():
            try:
                width = int(param.width.text())
            height = int(param.height.text())
            color = tuple(param.color)
            return True, width, height, color
        return False, None, None, None
    
    
    def uniform_image(self):
        ok, width, height, color = self.get_basic_params()
        if ok:
            if width == '' or height == None or color == None:
                text = 'You need to specify width, height and color in order to create a uniform image'
                msgBox = QMessageBox(self)
                msgBox.setText(text)
                msgBox.exec_()
                pass
            else:
                im = Image.create_uniform(width, height, color)
                self.add_image(im)
            
    def gaussian_filter(self):
        if self.cur_image == None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = GaussianImageDialog(self)
            if param.exec_():
                sigma = float(param.sigma.text())
                filtered_img = self.cur_image.gaussian(sigma)
                self.add_image(filtered_img)           
        
    def countouring(self):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
    def segmentation(self):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
    def create_histogram(self):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
    def procedural_image(self):
        name = self.sender().text()
        im = Image.create_procedural(name)
        self.add_image(im)

    def rasterize_image(self):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
    
    def select_action(self, name):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()
    
    def render_current(self):
        self.central.render_image(self.cur_image)
        
    def add_image(self, im):
        self.images.append(im)
        self.cur_image = im
        self.render_current()
        addimageAction = QAction(QIcon('segmentation.png'), im.title, self)
        addimageAction.triggered.connect(self.render_current)
        self.menuSelection.addAction(addimageAction)

if __name__=='__main__':
    app = QApplication(sys.argv)
    p = MainWindow()
    sys.exit(app.exec_())
    
