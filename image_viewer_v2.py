""" AUTHOR: GABRIEL GARCIA & ARNAU PERA"""
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
        self.menuDenoising = self.menuFilter.addMenu('Denoising')
        "Action Add Noise"
        noiseAction = QAction(QIcon('gaussian.png'),'Add Noise', self)
        noiseAction.triggered.connect(self.add_noise)
        self.menuDenoising.addAction(noiseAction)
        "Action Gaussian blurring"
        gaussianAction = QAction(QIcon('gaussian.png'),'Gaussian', self)
        gaussianAction.triggered.connect(self.gaussian_filter)
        self.menuDenoising.addAction(gaussianAction)
        "Action Billateral filtering"
        billateralAction = QAction(QIcon('gaussian.png'),'Billateral', self)
        billateralAction.triggered.connect(self.billateral_filter)
        self.menuDenoising.addAction(billateralAction)
        "Action Tv-Chambolle filtering"
        chambolleAction = QAction(QIcon('gaussian.png'),'Tv-Chambolle', self)
        chambolleAction.triggered.connect(self.chambolle_filter)
        self.menuDenoising.addAction(chambolleAction)
        "Action wavelet transforms filtering"
        waveletAction = QAction(QIcon('gaussian.png'),'Wavelet', self)
        waveletAction.triggered.connect(self.wavelet_filter)
        self.menuDenoising.addAction(waveletAction)
        "Action Contrast Stretching"
        ContrastStretchAction = QAction(QIcon('gaussian.png'),'Stretch Contrast', self)
        ContrastStretchAction.triggered.connect(self.contrast_stretch)
        self.menuFilter.addAction(ContrastStretchAction)
        "Submenu Contouring"
        self.menuContouring = self.menuFilter.addMenu('Countouring')
        "Action contouring"
        sobelAction = QAction(QIcon('contouring.png'),'Sobel Edge Detection', self)
        sobelAction.triggered.connect(self.sobel_filter)
        self.menuContouring.addAction(sobelAction)
        "Morphology"
        MorphologyAction = QAction(QIcon('contouring.png'),'Morphology', self)
        MorphologyAction.triggered.connect(self.morphology)
        self.menuFilter.addAction(MorphologyAction)
        "Submenu Segmentation"
        self.menuSegmentation = self.menuFilter.addMenu('Segmentation')
        "Action  Simple user-given threshold segmentation"
        usersegmentationAction = QAction(QIcon('segmentation.png'),'User-given threshold', self)
        usersegmentationAction.triggered.connect(self.user_segmentation)
        self.menuSegmentation.addAction(usersegmentationAction)
        "Action Otsu segmentation"
        otsusegmentationAction = QAction(QIcon('segmentation.png'),'Otsu threshold', self)
        otsusegmentationAction.triggered.connect(self.otsu_segmentation)
        self.menuSegmentation.addAction(otsusegmentationAction)

        
    def create_selection_menu(self):
        self.menuSelection = self.menubar.addMenu('Selection')
        for i in range(len(self.images)):
            im = self.images[i]
            selectImageAction = QAction(im.title, self)
            selectImageAction.triggered.connect(self.select_action)
            self.menuSelection.addAction(selectImageAction)
            
       
    def create_file_menu(self):
        self.menuFile = self.menubar.addMenu('File')

        readImageAction = QAction(QIcon('read.png'), 'Read image', self)
        readImageAction.setShortcut('Ctrl+F')
        readImageAction.triggered.connect(self.read_image)
        self.menuFile.addAction(readImageAction)

        SaveImageAction = QAction(QIcon('read.png'), 'Save current image', self)
        SaveImageAction.setShortcut('Ctrl+S')
        SaveImageAction.triggered.connect(self.save_image)
        self.menuFile.addAction(SaveImageAction)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.menuFile.addAction(exitAction)

    def create_tools_menu(self):
        self.menuTools = self.menubar.addMenu('Tools')
        """Histogram Action"""
        histogramAction = QAction(QIcon('resources/icons.png'), 'Histogram', self)
        histogramAction.triggered.connect(self.create_histogram)
        self.menuTools.addAction(histogramAction)
        """Contouring Action"""
        contouringAction = QAction(QIcon('resources/icons.png'), 'Find Contours', self)
        contouringAction.triggered.connect(self.contours)
        self.menuTools.addAction(contouringAction)

    def create_image_menu(self):
        self.menuImage = self.menubar.addMenu('Images')
        self.menuProcedural = self.menuImage.addMenu('Procedural')
        dict_list = self.call_dict()
        """Procedural Action"""
        for image in dict_list:
            dictAction = QAction(QIcon('dict.png'), image, self)
            dictAction.triggered.connect(self.procedural_image)
            self.menuProcedural.addAction(dictAction)
        """Uniform Action"""
        uniformAction = QAction(QIcon('resources/icons.png'), 'Uniform', self)
        uniformAction.setShortcut('Ctrl+H')
        uniformAction.triggered.connect(self.uniform_image)
        self.menuImage.addAction(uniformAction)
        """Rasterize Action"""
        rasterizeAction = QAction(QIcon('resources/icons.png'), 'Rasterization', self)
        rasterizeAction.triggered.connect(self.rasterize_image)
        self.menuImage.addAction(rasterizeAction)
        """Clip Circle Action"""
        ClipCircleAction = QAction(QIcon('resources/icons.png'), 'Clip Circle', self)
        ClipCircleAction.triggered.connect(self.clip_circle)
        self.menuImage.addAction(ClipCircleAction)


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
            except ValueError:
                width = None
            try:
                height = int(param.height.text())
            except ValueError:
                height = None
            try:
                color = tuple(param.color)
            except TypeError:
                color = None
            return True, width, height, color
        return False, None, None, None
    
    
    def uniform_image(self):
        ok, width, height, color = self.get_basic_params()
        if ok:
            if width is None or height is None or color is None:
                text = 'You need to specify a correct width, height and color in order to create a uniform image'
                msgBox = QMessageBox(self)
                msgBox.setWindowTitle("Error! Missing or wrong parameters!")
                msgBox.setText(text)
                msgBox.exec_()
            else:
                im = Image.create_uniform(width, height, color)
                self.add_image(im)
            
    def gaussian_filter(self):
        if self.cur_image is None:
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

    def billateral_filter(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
           filtered_img = self.cur_image.billateral()
           self.add_image(filtered_img)

    def chambolle_filter(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = ChambolleImageDialog(self)
            if param.exec_():
                weight = float(param.weight.text())
                epsilon = float(param.epsilon.text())
                filtered_img = self.cur_image.chambolle(weight, epsilon)
                self.add_image(filtered_img)

    def wavelet_filter(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            filtered_img = self.cur_image.wavelet()
            self.add_image(filtered_img)

    def add_noise(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = NoiseImageDialog(self)
            if param.exec_():
                sigma = float(param.sigma.text())
                filtered_img = self.cur_image.add_noise(sigma)
                self.add_image(filtered_img)

    def countouring(self):
        text = 'Option in progress sorry'
        msgBox = QMessageBox(self)
        msgBox.setText(text)
        msgBox.exec_()

    def user_segmentation(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = UserThresholdImageDialog(self)
            if param.exec_():
                threshold = float(param.threshold.text())
                filtered_img = self.cur_image.user_threshold(threshold)
                self.add_image(filtered_img)

    def otsu_segmentation(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
           filtered_img = self.cur_image.otsu_threshold()
           self.add_image(filtered_img)

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
    
    def select_action(self):
        name = self.sender().text()
        dicc = self.diccionario()
        index = dicc[name]
        self.cur_image = self.images[index]
        self.render_current()
    
    def render_current(self):
        self.central.render_image(self.cur_image)

    def diccionario(self):
        dicc = {}
        n = 0
        for im in self.images:
            dicc[im.title] = n
            n = n +1
        return dicc
        
    def add_image(self, im):
        self.images.append(im)
        self.cur_image = im
        self.render_current()
        addimageAction = QAction(QIcon('segmentation.png'), im.title, self)
        addimageAction.triggered.connect(self.select_action)
        self.menuSelection.addAction(addimageAction)


    def call_dict(self):
        dict_list = Image.call_proc_dict()
        return dict_list

    def sobel_filter(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = SobelImageDialog(self)
            if param.exec_():
                direction = param.direction
                filtered_img = self.cur_image.sobel_filter(direction)
                self.add_image(filtered_img)

    def clip_circle(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = ClipCircleImageDialog(self)
            if param.exec_():
                center = (int(param.centerx.text()), int(param.centery.text()))
                radius = int(param.radius.text())
                filtered_img = self.cur_image.clip_circle(center, radius)
                self.add_image(filtered_img)
    def contours(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            filtered_img = self.cur_image.find_contours
            self.add_image(filtered_img)

    def contrast_stretch(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = ContrastStretchImageDialog(self)
            pmin = 0
            pmax = 100
            if param.exec_():
                try:
                    pmin = int(param.pmin.text())
                    if pmin < 0 or pmin > 100:
                        text = 'Minimum percentile should be a number between 0 and 100'
                        msgBox = QMessageBox(self)
                        msgBox.setText(text)
                        msgBox.exec_()
                except ValueError:
                    text = 'Percentiles should be a number between 0 and 100'
                    msgBox = QMessageBox(self)
                    msgBox.setText(text)
                    msgBox.exec_()
                try:
                    pmax = int(param.pmax.text())
                    if pmax < 0 or pmax > 100:
                        text = 'Maximum percentile should be a number between 0 and 100'
                        msgBox = QMessageBox(self)
                        msgBox.setText(text)
                        msgBox.exec_()
                except ValueError:
                    text = 'Percentiles should be a number between 0 and 100'
                    msgBox = QMessageBox(self)
                    msgBox.setText(text)
                    msgBox.exec_()
                filtered_img = self.cur_image.contrast_stretch(pmin, pmax)
                self.add_image(filtered_img)

    def save_image(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = SaveImageDialog(self)
            filename = 'currentimage'
            if param.exec_():
                filename = param.filename.text()+'.ppm'
                self.cur_image.save_ppm(filename)
                text = 'Saved correctly as '+filename
                msgBox = QMessageBox(self)
                msgBox.setText(text)
                msgBox.exec_()

    def morphology(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            param = MorphologyImageDialog(self)
            if param.exec_():
                direction = param.direction
                if direction == 'none':
                    text = 'Please select a morphology type'
                    msgBox = QMessageBox(self)
                    msgBox.setText(text)
                    msgBox.exec_()
                else:
                    filtered_img = self.cur_image.morphology(direction)
                    self.add_image(filtered_img)

if __name__=='__main__':
    app = QApplication(sys.argv)
    p = MainWindow()
    sys.exit(app.exec_())
