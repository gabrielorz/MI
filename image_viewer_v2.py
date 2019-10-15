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
from paramdialog import ParamImageDialog
from polygonlist import PolygonList

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
        self.create_selection_menu()
        self.create_filter_menu()
        self.create_help_menu()

    def create_filter_menu(self):
        self.menuFilter = self.menubar.addMenu('Filter')
    
    def create_selection_menu(self):
        self.menuSelection = self.menubar.addMenu('Selection')
        
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

    def create_image_menu(self):
        self.menuImage = self.menubar.addMenu('Images')

        self.menuProcedural = self.menuImage.addMenu('Procedural')
        """
        Add all the options of the procedural image creation
        """
        uniformAction = QAction(QIcon('resources/icons.png'), 'Uniform', self)  
        uniformAction.setShortcut('Ctrl+H')
        uniformAction.triggered.connect(self.uniform_image)
        self.menuImage.addAction(uniformAction)

        """ 
        Add rasterization and all other image creation you'll implement 
        """
        

    def create_help_menu(self):
        self.menuHelp = self.menubar.addMenu('Help')
        helpAction = QAction(QIcon('resources/icons.png'), 'Help', self)  
        helpAction.setShortcut('Ctrl+H')
        helpAction.triggered.connect(self.help_action)
        self.menuHelp.addAction(helpAction)

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
        text = 'Image viewer by DaniTost@CREB'
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
            width = int(param.width.text())
            height = int(param.height.text())
            color = 255, 0, 0   # change that when you'll add a color selector in the widget
            return True, width, height, color
        return False, None, None, None
    
    def uniform_image(self):
        ok, width, height, color = self.get_basic_params()
        if ok:
            im = Image.create_uniform( width, height, color)
            self.add_image(im)

    def procedural_image(self):
        name = self.sender().text()
        im = Image.create_procedural(name)
        self.add_image(im)

    def rasterize_image(self):
        """
        To be implemented
        """
        pass
    
    def select_action(self, name):
        """
        To be implemented
        """
        pass
    
    def render_current(self):
        self.central.render_image(self.cur_image)
        
    def add_image(self, im):
        self.images.append(im)
        self.cur_image = im
        self.render_current()
        """
        Add the name of the image in the selction menu
        """

if __name__=='__main__':
    app = QApplication(sys.argv)
    p = MainWindow()
    sys.exit(app.exec_())
    
