"""
MUEI- ETSEIB
Medical images- Cur 2019-20-Q1
Dani Tost

image_viewer_v3.py: example of a PyQt interface with a matplotlib widegt and a vtkwidget

"""
import vtk
import sys

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QAction, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon
from paramdialog import SphereDialog

from central import CentralWidget
from scene import Scene
from image import Image
from surface import Surface
from volume import Volume


class MainWindow(QMainWindow):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.scene = Scene()
        self.initUI()
        
    def initUI(self):
        self.create_menus()
        self.central = CentralWidget(self.scene)
        self.setCentralWidget(self.central)

        self.show()
        
    def create_menus(self) :
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.create_file_menu()
        self.create_image_menu()
        self.create_surface_menu()
        self.create_volume_menu()
        self.create_help_menu()


    def create_image_menu(self):
        self.menuImage = self.menubar.addMenu('Images')
        self.menuProcedural = self.menuImage.addMenu('Procedural')
        for name in Image.dic_procedural:
            proceduralAction = QAction(QIcon('resources/icons.png'), name, self)  
            proceduralAction.triggered.connect(self.procedural_image)
            self.menuProcedural.addAction(proceduralAction)
        self.menuImageSelection = self.menuImage.addMenu('Select')
        
    def create_surface_menu(self):
        self.menuSurface = self.menubar.addMenu('Surfaces')
        sphereAction = QAction(QIcon('resources/icons.png'), 'Create sphere', self)  
        sphereAction.triggered.connect(self.sphere)
        self.menuSurface.addAction(sphereAction)
        mcAction = QAction(QIcon('resources/icons.png'), 'Extract from volume', self)  
        mcAction.triggered.connect(self.extract_surface)
        self.menuSurface.addAction(mcAction)
        self.menuSurfaceSelection = self.menuSurface.addMenu('Select')
    
    def create_volume_menu(self):
        self.menuVolume = self.menubar.addMenu('Volumes')                
        self.menuVolume.addSeparator()
        self.menuVolumeSelection = self.menuVolume.addMenu('Select')

    def create_file_menu(self):
        self.menuFile = self.menubar.addMenu('File')

        readImageAction = QAction(QIcon('read.png'), 'Read image', self)  
        readImageAction.setShortcut('Ctrl+F')
        readImageAction.triggered.connect(self.read_image)
        self.menuFile.addAction(readImageAction)

        readSurfaceAction = QAction(QIcon('read.png'), 'Read surface', self)  
        readSurfaceAction.triggered.connect(self.read_surface)
        self.menuFile.addAction(readSurfaceAction)
        
        readVolumeAction = QAction(QIcon('read.png'), 'Read volume', self)  
        readVolumeAction.triggered.connect(self.read_volume)
        self.menuFile.addAction(readVolumeAction)
        
        self.menuFile.addSeparator()
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)  
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.menuFile.addAction(exitAction)

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
    
    def read_surface(self) :
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self,"Read surface file", "","", options=options)
        if ok:
            surface = Surface.read_file(filename, self.scene.material('surface_default'))
            if surface != None :
                self.add_surface(surface)
            else:
                reply = QMessageBox.warning(self, 'Error', "Unable to read {}".format(filename))
                return

    def read_volume(self) :
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self,"Read volume file", "","", options=options)
        if ok:
            volume = Volume.read_file(filename,  self.scene.material('volume_default'))
            if volume != None :
                self.add_volume(volume)
            else:
                reply = QMessageBox.warning(self, 'Error', "Something went wrong")                

    def extract_surface(self):
        vol = self.scene.cur_volume 
        if vol == None:
            reply = QMessageBox.warning(self, 'Error', "No current volume loaded")
            return
        # Put a dialog to get vmin and vmax instead of fixed values 0 70 (suitable for mummy.vtk
        vmin = 0
        vmax = 70
        surf = Surface.from_volume(vol, (vmin, vmax),  self.scene.material('surface_default'))
        if surf != None:
            self.add_surface(surf)
        else:
            reply = QMessageBox.warning(self, 'Error', "Something went wrong")
            
    def procedural_image(self):
        name = self.sender().text()
        im = Image.create_procedural(name)
        self.add_image(im)

    def sphere(self) :
        param = SphereDialog(self)
        if param.exec_():
            cx = float(param.x.text())
            cy = float(param.y.text())
            cz = float(param.z.text())
            rad =  float(param.radius.text())
            rh =  int(param.resh.text())
            rv =  int(param.resv.text())
            surface = Surface.from_sphere((cx, cy, cz), rad, (rh, rv), self.scene.material('surface_default'))
            if surface != None :
                self.add_surface(surface)
                
        
    def select_image_action(self):
        img = self.sender().text()
        self.scene.cur_image = self.scene.images.get_object(img)
        self.render_current_image()
        self.statusBar().showMessage(img)

    def select_surface_action(self):
        surf = self.sender().text()
        self.scene.cur_surface = self.scene.surfaces.get_object(surf)
        self.render_current_surface()
        self.statusBar().showMessage(surf)

    def select_volume_action(self):
        vol = self.sender().text()
        self.scene.cur_volume = self.scene.volumes.get_object(vol)
        self.render_current_volume()
        self.statusBar().showMessage(vol)        
        
    def render_current_image(self):
        self.central.render_image(self.scene.cur_image)

    def render_current_surface(self):
        self.central.render_surface(self.scene.cur_surface)

    def render_current_volume(self):
        self.central.render_volume(self.scene.cur_volume)        

    def add_image(self, im):
        self.scene.images.append(im)
        self.scene.cur_image = im
        itemAction = QAction(im.name, self)
        itemAction.triggered.connect(self.select_image_action)
        self.menuImageSelection.addAction(itemAction)
        self.render_current_image()

    def add_surface(self, surf):
        self.scene.surfaces.append(surf)
        self.scene.cur_surface = surf
        itemAction = QAction(surf.name, self)
        itemAction.triggered.connect(self.select_surface_action)
        self.menuSurfaceSelection.addAction(itemAction)
        self.render_current_surface()

    def add_volume(self, vol):
        self.scene.volumes.append(vol)
        self.scene.cur_volume = vol
        itemAction = QAction(vol.name, self)
        itemAction.triggered.connect(self.select_volume_action)
        self.menuVolumeSelection.addAction(itemAction)
        self.render_current_volume()
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    p = MainWindow()
    sys.exit(app.exec_())
    
