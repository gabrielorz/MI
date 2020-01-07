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
from surface import Surface
from scene import Scene
from volume import Volume
import vtk

class MainWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.images = ImageList()
        self.cur_image= None   # The one visible
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
        """self.create_transfer_function_menu()"""
        self.create_tools_menu()
        self.create_selection_menu()
        self.create_filter_menu()
        self.create_help_menu()

    """def create_transfer_function_menu(self):
        self.menuTF = self.menubar.addMenu('Transfer Functions')
        bronzeAction = QAction(QIcon('resources/icons.png'), 'Bronze', self)
        bronzeAction.triggered.connect(self.scene.material('bronze'))
        self.menuTF.addAction(bronzeAction)"""

    def create_surface_menu(self):
        self.menuSurface = self.menubar.addMenu('Surfaces')
        mcAction = QAction(QIcon('resources/icons.png'), 'Extract from volume', self)
        mcAction.triggered.connect(self.extract_surface)
        self.menuSurface.addAction(mcAction)
        self.menuSurfaceSelection = self.menuSurface.addMenu('Select')

        """ Predefined surfaces"""
        self.menuPredSurf = self.menuSurface.addMenu('Predefined surfaces')

        """Sphere"""
        sphereAction = QAction(QIcon('resources/icons.png'), 'CSphere', self)
        sphereAction.triggered.connect(self.sphere)
        self.menuPredSurf.addAction(sphereAction)
        """Mobius"""
        mobiusAction = QAction(QIcon('resources/icons.png'), 'Mobius', self)
        mobiusAction.triggered.connect(self.mobius)
        self.menuPredSurf.addAction(mobiusAction)

        """Conic Spiral"""
        conicspiralAction = QAction(QIcon('resources/icons.png'), 'Conic Spiral', self)
        conicspiralAction.triggered.connect(self.conicspiral)
        self.menuPredSurf.addAction(conicspiralAction)

        """Boy"""
        boyAction = QAction(QIcon('resources/icons.png'), 'Boy', self)
        boyAction.triggered.connect(self.boy)
        self.menuPredSurf.addAction(boyAction)

        """Cross Cap"""
        crosscapAction = QAction(QIcon('resources/icons.png'), 'Cross Cap', self)
        crosscapAction.triggered.connect(self.crosscap)
        self.menuPredSurf.addAction(crosscapAction)

        STLSaveAction = QAction(QIcon('resources/icons.png'), 'Save stl', self)
        STLSaveAction.triggered.connect(self.saveSTL)
        self.menuSurface.addAction(STLSaveAction)

    def create_volume_menu(self):
        self.menuVolume = self.menubar.addMenu('Volumes')
        self.menuVolume.addSeparator()
        self.menuVolumeSelection = self.menuVolume.addMenu('Select')


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
        "Action Histogram Equalization"
        EquAction = QAction(QIcon('resources/icons.png'), 'Histogram Equalization', self)
        EquAction.triggered.connect(self.histogram_equalization)
        self.menuFilter.addAction(EquAction)

        
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

        readSurfaceAction = QAction(QIcon('read.png'), 'Read surface', self)
        readSurfaceAction.triggered.connect(self.read_surface)
        self.menuFile.addAction(readSurfaceAction)

        readVolumeAction = QAction(QIcon('read.png'), 'Read volume', self)
        readVolumeAction.triggered.connect(self.read_volume)
        self.menuFile.addAction(readVolumeAction)

        self.menuFile.addSeparator()

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
        uniformAction.setShortcut('Ctrl+U')
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

    def get_basic_params_raster(self):
        param = PolygonImageDialog(self)
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
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            filtered_img = self.cur_image.create_histogram()
            self.add_image(filtered_img)

    def histogram_equalization(self):
        if self.cur_image is None:
            text = 'There is no current Image'
            msgBox = QMessageBox(self)
            msgBox.setText(text)
            msgBox.exec_()
        else:
            filtered_img = self.cur_image.histogram_equalization()
            self.add_image(filtered_img)

    def procedural_image(self):
        name = self.sender().text()
        im = Image.create_procedural(name)
        self.add_image(im)

    def rasterize_image(self):
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self, "Read image file", "", "", options=options)
        if ok:
            plist = PolygonList.FromJson(filename)
            ok, width, height, color = self.get_basic_params_raster()
            if ok:
                self.add_image(Image.create_rasterization(width, height, color, plist, 'rasterization'))

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
            n = n + 1
        return dicc
        
    def add_image(self, im):
        n = 1
        dicc = self.diccionario()
        while im.title in dicc:
            cifras = len(str(n))
            if n > 1:
                im.title = im.title[:-cifras-1]
            im.title = im.title + '_' + str(n)
            n = n + 1
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
            param = UserThresholdImageDialog(self)
            if param.exec_():
                try:
                    threshold = float(param.threshold.text())
                    filtered_img = self.cur_image.find_contours(threshold)
                    self.add_image(filtered_img)
                except ValueError:
                    text = 'Please insert a number'
                    msgBox = QMessageBox(self)
                    msgBox.setText(text)
                    msgBox.exec_()

            """self.render_current()"""

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

    def read_surface(self) :
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self,"Read surface file", "", "", options=options)
        param = SurfaceMaterialDialog(self)
        if param.exec_():
            color = param.direction
        else:
            color = 'default_surface'
        if ok:
            surface = Surface.read_file(filename, self.scene.material(color))
            if surface is not None:
                self.add_surface(surface)
            else:
                reply = QMessageBox.warning(self, 'Error', "Unable to read {}".format(filename))
                return

    def read_volume(self):
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getOpenFileName(self,"Read volume file", "", "", options=options)
        if ok:
            volume = Volume.read_file(filename,  self.scene.material('volume_default'))
            if volume is not None:
                self.add_volume(volume)
            else:
                reply = QMessageBox.warning(self, 'Error', "Something went wrong")

    def extract_surface(self):
        vol = self.scene.cur_volume
        param = ExtractSurfaceDialog(self)
        if param.exec_():
            vmin = int(param.vmin.text())
            vmax = int(param.vmax.text())
        else:
            vmin = 0
            vmax = 70
        if vol is None:
            reply = QMessageBox.warning(self, 'Error', "No current volume loaded")
            return
        # Put a dialog to get vmin and vmax instead of fixed values 0 70 (suitable for mummy.vtk

        surf = Surface.from_volume(vol, (vmin, vmax),  self.scene.material('surface_default'))
        if surf is not None:
            self.add_surface(surf)
        else:
            reply = QMessageBox.warning(self, 'Error', "Something went wrong")

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

    """def add_image(self, im):
        self.scene.images.append(im)
        self.scene.cur_image = im
        itemAction = QAction(im.name, self)
        itemAction.triggered.connect(self.select_image_action)
        self.menuImageSelection.addAction(itemAction)
        self.render_current_image()"""

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

    def sphere(self) :
        param = SphereDialog(self)
        if param.exec_():
            cx = float(param.x.text())
            cy = float(param.y.text())
            cz = float(param.z.text())
            rad = float(param.radius.text())
            rh = int(param.resh.text())
            rv = int(param.resv.text())
            surface = Surface.from_sphere((cx, cy, cz), rad, (rh, rv), self.scene.material('surface_default'))
            if surface is not None:
                self.add_surface(surface)

    def mobius(self):
        surface = Surface.from_mobius(mat=None)
        if surface is not None:
            self.add_surface(surface)

    def conicspiral(self):
        surface = Surface.from_conicspiral(mat=None)
        if surface is not None:
            self.add_surface(surface)

    def boy(self):
        surface = Surface.from_boy(mat=None)
        if surface is not None:
            self.add_surface(surface)

    def crosscap(self):
        surface = Surface.from_crosscap(mat=None)
        if surface is not None:
            self.add_surface(surface)

    def saveSTL(self):
        stlWriter = vtk.vtkSTLWriter()
        options = QFileDialog.Options()
        filename, ok = QFileDialog.getSaveFileName(self,"Save surface as", "","",options=options)
        if ok:
            filename = filename+'stl'
            stlWriter.SetFileName(filename)
            stlWriter.SetInputConnection(self.scene.cur_surface.source.GetOutputPort())
            stlWriter.Write()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    p = MainWindow()
    sys.exit(app.exec_())
