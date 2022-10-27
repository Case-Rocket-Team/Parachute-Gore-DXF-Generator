# Parachute Gore DXF Generator
# Copyright © 2022 Eabha Abramson
# gui.py - Contains all of the code needed to run the GUI and keep track of its values

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from pyqtgraph.widgets.PlotWidget import PlotWidget
from config import *
from functions import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QDoubleSpinBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QVBoxLayout, QWidget
import sys
import ctypes
import pyqtgraph

# Set pyqtgraph display options
pyqtgraph.setConfigOptions(background="w", foreground="k",antialias=True)

class DropdownBox(QWidget):

    "A class containing a QComboBox and a label for the box."

    def __init__(self, title: str, options: list[str]) -> None:
        super().__init__()
        
        # Create label and box
        self.__label = QLabel()
        self.__box = QComboBox()

        # Populate initial values
        self.label().setText(title)
        self.box().addItems(options)
        self.box().setCurrentText(options[0])

        # Set up horizontal layout
        layout = QHBoxLayout()
        layout.addWidget(self.label())
        layout.addWidget(self.box())
        self.setLayout(layout)

    def label(self):
        return self.__label
    
    def box(self):
        return self.__box
    
    def value(self):
        return self.box().currentText()

class SliderWithBox(QWidget):

    "A class containing a QLabel, a QSlider, and a QSpinBox. The QSlider and QSpinBox have their values synchronized."
    
    def __init__(self, title: str, min: int, max: int, step: float):
        super().__init__()

        # Create label, slider, box, and vertical layout
        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__slider = QSlider(Qt.Horizontal)
        self.__box = QSpinBox()

        # Populate initial values
        self.label().setText(title)
        self.slider().setRange(min, max)
        self.slider().setSingleStep(step)
        self.box().setRange(min, 1000)
        self.box().setValue(self.slider().value())

        # Place the label at the top of the layout. Create a horizontal layout with the slider and the box and place it at the bottom of the layout
        self.layout().addWidget(self.label())
        layout = QHBoxLayout()
        layout.addWidget(self.slider())
        layout.addWidget(self.box())
        self.layout().addLayout(layout)

        # Set box and slider to update each other
        self.slider().sliderMoved.connect(self.sliderHandleMoved)
        self.box().valueChanged.connect(self.boxValueChanged)
        
    
    def label(self):
        return self.__label

    def slider(self):
        return self.__slider

    def box(self):
        return self.__box
    
    def setBox(self, box):
        self.__box = box
    
    def value(self):
        return self.box().value()
    
    def setValue(self, value):
        "Sets the value for the box and the slider properly"
        self.slider().setValue(value)
        self.box().setValue(value)
    
    def sliderHandleMoved(self, value):
        "Updates the box when the slider is moved"
        self.box().setValue(value)
    
    def boxValueChanged(self, value):
        "Updates the slider when the box value is changed"
        self.slider().setValue(value)

class SliderWithDoubleBox(QWidget):

    "A class containing a QLabel, a QSlider, and a QSDoublepinBox. The QSlider and QDoubleSpinBox have their values synchronized."
    
    def __init__(self, title: str, min: int, max: int, step: float):
        super().__init__()

        # Create label, slider, box, and vertical layout
        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__slider = QSlider(Qt.Horizontal)
        self.__box = QDoubleSpinBox()

        # Populate initial values
        self.label().setText(title)
        self.slider().setRange(min, max)
        self.slider().setSingleStep(step)
        self.box().setRange(min, 1000)
        self.box().setValue(self.slider().value())

        # Place the label at the top of the layout. Create a horizontal layout with the slider and the box and place it at the bottom of the layout
        self.layout().addWidget(self.label())
        layout = QHBoxLayout()
        layout.addWidget(self.slider())
        layout.addWidget(self.box())
        self.layout().addLayout(layout)

        # Set box and slider to update each other
        self.slider().sliderMoved.connect(self.sliderHandleMoved)
        self.box().valueChanged.connect(self.boxValueChanged)
        
    
    def label(self):
        return self.__label

    def slider(self):
        return self.__slider

    def box(self):
        return self.__box
    
    def setBox(self, box):
        self.__box = box
    
    def value(self):
        return self.box().value()
    
    def setValue(self, value):
        "Sets the value for the box and the slider properly"
        self.slider().setValue(value)
        self.box().setValue(value)
    
    def sliderHandleMoved(self,value):
        "Updates the box when the slider is moved"
        self.box().setValue(value)
    
    def boxValueChanged(self, value):
        "Updates the slider when the box value is changed"
        self.slider().setValue(value)

class DoubleBoxWithLabel(QWidget):

    "A class specifically designed to take in a hem allowance value, containing a QLabel and a QDoubleSpinBox."

    def __init__(self, name: str, min: float, max: float, step: float):
        super().__init__()

        # Create label, box, and horizontal layout
        self.setLayout(QHBoxLayout())
        self.__label = QLabel()
        self.__box = QDoubleSpinBox()

        # Populate initial values
        self.label().setText(name)
        self.box().setRange(min, max)
        self.box().setSingleStep(step)

        # Set up horizontal layout
        self.layout().addWidget(self.label())
        self.layout().addWidget(self.box())
    
    def label(self):
        return self.__label
    
    def box(self):
        return self.__box

class FolderBox(QWidget):

    "A class containing a label, a text box, and a button to choose a folder for the output file"

    def __init__(self, default: str=""):
        super().__init__()

        # Create label, box, button, and layout
        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__box = QLineEdit()
        self.__button = QPushButton()

        # Populate initial values
        self.label().setText("Output Folder")
        self.button().setText("Choose folder...")

        # Set up horizontal layout
        layout = QHBoxLayout()
        layout.addWidget(self.label())
        layout.addWidget(self.button())
        self.layout().addLayout(layout)
        self.layout().addWidget(self.box())

    def label(self):
        return self.__label
    
    def box(self):
        return self.__box
    
    def button(self):
        return self.__button

class FilenameBox(QWidget):

    "A class containing a label and a text box, designed to accept a name for an output file (or supply a default if none is porvided)"

    def __init__(self, default: str=""):
        super().__init__()
        # Create label, box, and layout
        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__box = QLineEdit()

        # Populate initial values
        self.label().setText("File Name (leave blank for default)")

        # Set up horizontal layout
        self.layout().addWidget(self.label())
        self.layout().addWidget(self.box())

    def label(self):
        return self.__label
    
    def box(self):
        return self.__box

class UpdateButton(QPushButton):

    "A button for requesting a plot of a parachute gore"

    def __init__(self):
        super().__init__()
        self.setText("Plot gore")
       
class GetDXFButton(QPushButton):

    "A class for requesting a dxf file containing a parachute gore pattern"

    def __init__(self):
        super().__init__()
        self.setText("Get DXF")

class OptionsPane(QWidget):

    "The options pane for the program (i.e. everything except the graph and logo). This class creates the required options inputs and sets starting values"

    def __init__(self):
        super().__init__()

        # Create the input classes (boxes, sliders, buttons, etc.)
        self.__chute_profile_dropdown = DropdownBox("Chute Profile", ["Elliptical", "Toroidal"])
        self.__diameter_slider = SliderWithBox("Diameter", 6, 96, 2)
        self.__inner_diameter_slider = SliderWithBox("Inner Diameter", 0, DIAMETER-1, 1)
        self.__height_ratio_box = DoubleBoxWithLabel("Height Ratio", 0, 1, 0.001)
        self.__pulldown_ratio_box = DoubleBoxWithLabel("Pulldown Ratio", 0, 1, 0.01)
        self.__num_gores_slider = SliderWithBox("Number of Gores", 4, 20, 1)
        self.__allowance_box = DoubleBoxWithLabel("Allowance", 0, 2, 0.05)
        self.__model_type_dropdown = DropdownBox("Model Type", ["Polygonal", "Circular"])
        self.__units_dropdown = DropdownBox("Units", ["Inches", "Centimeters"])
        self.__folder_box = FolderBox()
        self.__filename_box = FilenameBox()
        self.__update_button = UpdateButton()
        self.__get_dxf_button = GetDXFButton()

        # Configure GUI items
        self.heightRatioBox().box().setDecimals(3)

        # Populate initial values
        self.chuteProfileDropdown().box().setCurrentIndex(int(PROFILE))
        self.diameterSlider().setValue(int(DIAMETER))
        self.innerDiameterSlider().setValue(int(INNER_DIAMETER))
        self.heightRatioBox().box().setValue(RATIO)
        self.pulldownRatioBox().box().setValue(PULLDOWN_RATIO)
        self.numGoresSlider().setValue(int(NUM_GORES))
        self.modelTypeDropdown().box().setCurrentIndex(MODEL_TYPE)
        self.unitsDropdown().box().setCurrentIndex(UNITS_INDEX)
        self.allowanceBox().box().setValue(float(ALLOWANCE))

        # Set up the layout of the options pane
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.chuteProfileDropdown())
        layout.addWidget(self.diameterSlider())
        layout.addWidget(self.innerDiameterSlider())
        layout.addWidget(self.heightRatioBox())
        layout.addWidget(self.pulldownRatioBox())
        layout.addWidget(self.numGoresSlider())
        layout.addWidget(self.allowanceBox())
        layout.addWidget(self.modelTypeDropdown())
        layout.addWidget(self.unitsDropdown())
        layout.addWidget(self.folderBox())
        layout.addWidget(self.filenameBox())
        layout.addWidget(self.updateButton())
        layout.addWidget(self.getDXFButton())
    
    def chuteProfileDropdown(self):
        return self.__chute_profile_dropdown

    def diameterSlider(self):
        return self.__diameter_slider
    
    def innerDiameterSlider(self):
        return self.__inner_diameter_slider
    
    def heightRatioBox(self):
        return self.__height_ratio_box
    
    def pulldownRatioBox(self):
        return self.__pulldown_ratio_box
    
    def numGoresSlider(self):
        return self.__num_gores_slider
    
    def allowanceBox(self):
        return self.__allowance_box
    
    def modelTypeDropdown(self):
        return self.__model_type_dropdown
    
    def unitsDropdown(self):
        return self.__units_dropdown
    
    def folderBox(self):
        return self.__folder_box
    
    def filenameBox(self):
        return self.__filename_box
    
    def updateButton(self):
        return self.__update_button
    
    def getDXFButton(self):
        return self.__get_dxf_button

class MainWindow(QWidget):

    "The main window class for the program and the bulk of the overall program control. Creates an options pane, a gore plot, a logo, and a copyright label. Links the inputs to their respective functions and manages values"

    def __init__(self):
        super().__init__()

        # Calculate a logo and window size based on display resolution
        size = int(min(ctypes.windll.user32.GetSystemMetrics(0) / 16, ctypes.windll.user32.GetSystemMetrics(1) / 9))

        # Create options pane, plot, logo, label, and layout
        self.__layout = QHBoxLayout()
        self.__options_pane = OptionsPane()
        self.__plot = PlotWidget()
        self.__logo = QLabel()
        self.__copy = QLabel()

        # Set the gore plot axes to always be 1:1 proportion and show the grid
        self.plot().getPlotItem().getViewBox().setAspectLocked()
        self.plot().getPlotItem().showGrid(True, True, 0.6)

        # Add options pane to the layout. Create a vertical layout with the plot and logo and add it to the layout
        layout = QVBoxLayout()
        self.layout().addWidget(self.optionsPane())
        layout.addWidget(self.plot())
        layout.addWidget(self.__logo)
        layout.addWidget(self.__copy)
        self.layout().addLayout(layout)
        self.setLayout(self.layout())

        # Set the logo to a constant size based on display resolution
        self.logo().setPixmap(QPixmap("logo.png").scaled(size, size))
        self.logo().setAlignment(Qt.AlignHCenter)

        # Set the copyright label text
        self.copy().setText("Copyright © 2022 Eabha Abramson")
        self.copy().setAlignment(Qt.AlignHCenter)

        # Create chute parameters in the main window so the logic can access the values
        self.__profile = int(PROFILE)
        self.__diameter = float(DIAMETER)
        self.__inner_diameter = float(INNER_DIAMETER)
        self.__height_ratio = float(RATIO)
        self.__pulldown_ratio = float(PULLDOWN_RATIO)
        self.__num_gores = int(NUM_GORES)
        self.__allowance = float(ALLOWANCE)
        self.__model_type = int(MODEL_TYPE)
        self.__units = int(UNITS)
        self.__folder = str(FOLDER)
        self.__filename = str("{:.0f}".format(self.diameter()) + "{:02.0f}".format(self.innerDiameter()) + "-" + str(self.numGores()) + chute_profile[self.profile()] + chute_type[self.modelType()])
        self.__point_list = array(None)
        self.__offset_point_list = array(None)

        # Link option input value updates so that they update the values in the main window as well
        self.optionsPane().chuteProfileDropdown().box().currentIndexChanged.connect(self.profileChanged)
        self.optionsPane().diameterSlider().box().valueChanged.connect(self.diameterChanged)
        self.optionsPane().innerDiameterSlider().box().valueChanged.connect(self.innerDiameterChanged)
        self.optionsPane().heightRatioBox().box().valueChanged.connect(self.heightRatioChanged)
        self.optionsPane().pulldownRatioBox().box().valueChanged.connect(self.pulldownRatioChanged)
        self.optionsPane().numGoresSlider().box().valueChanged.connect(self.numGoresChanged)
        self.optionsPane().allowanceBox().box().valueChanged.connect(self.allowanceChanged)
        self.optionsPane().modelTypeDropdown().box().currentIndexChanged.connect(self.modelTypeChanged)
        self.optionsPane().unitsDropdown().box().currentTextChanged.connect(self.unitsChanged)
        self.optionsPane().folderBox().box().textChanged.connect(self.folderChanged)
        self.optionsPane().folderBox().button().clicked.connect(self.folderButtonClicked)
        self.optionsPane().filenameBox().box().textChanged.connect(self.filenameChanged)
        self.optionsPane().updateButton().clicked.connect(self.updateButtonClicked)
        self.optionsPane().getDXFButton().clicked.connect(self.getDXFButtonClicked)

        # Set the filename box background text to the default filename
        self.optionsPane().filenameBox().box().setPlaceholderText(self.filename())

        # Set window size based on display resolution
        width = int(size * 4)
        height = int(size * 9 / 2)
        self.resize(width, height)
    
    def layout(self):
        return self.__layout
    
    def optionsPane(self):
        return self.__options_pane
    
    def plot(self):
        return self.__plot
    
    def setPlot(self, plot):
        self.__plot = plot
    
    def logo(self):
        return self.__logo
    
    def copy(self):
        return self.__copy
    
    def profile(self):
        return self.__profile
    
    def diameter(self):
        return self.__diameter
    
    def innerDiameter(self):
        return self.__inner_diameter
    
    def heightRatio(self):
        return self.__height_ratio
    
    def pulldownRatio(self):
        return self.__pulldown_ratio
    
    def numGores(self):
        return self.__num_gores
    
    def allowance(self):
        return self.__allowance
    
    def modelType(self):
        return self.__model_type
    
    def units(self):
        return self.__units
    
    def folder(self):
        return self.__folder
    
    def filename(self):
        return self.__filename
    
    def pointList(self):
        return self.__point_list
    
    def setPointList(self, list: ndarray):
        self.__point_list = list
    
    def offsetPointList(self):
        return self.__offset_point_list
    
    def setOffsetPointList(self, list):
        self.__offset_point_list = list
    
    def profileChanged(self, value):
        "When the chute profile changes in the input box, update it in the main window as well"
        self.__profile = value
        self.updateDefaultFilename()
    
    def diameterChanged(self, value):
        "When the outer diameter changes in the input box, update it in the main window as well. Also, adjust the maximum inner diamter so it cannot be larger than the current diameter"
        self.__diameter = value
        self.optionsPane().innerDiameterSlider().slider().setMaximum(value-1)
        self.optionsPane().innerDiameterSlider().box().setMaximum(value-1)
        self.updateDefaultFilename()
    
    def innerDiameterChanged(self, value):
        "When the inner diameter changes in the input box, update it in the main window as well"
        self.__inner_diameter = value
        self.updateDefaultFilename()
    
    def heightRatioChanged(self, value):
        "When the height ratio changes in the input box, update it in the main window as well"
        self.__height_ratio = value

    def pulldownRatioChanged(self, value):
        "When the pulldown raio changes in the input box, update it in the main window as well"
        self.__pulldown_ratio = value
    
    def numGoresChanged(self, value):
        "When the number of gores changes in the input box, update it in the main window as well"
        self.__num_gores = value
        self.updateDefaultFilename()
    
    def allowanceChanged(self, value):
        "When the hem allowance changes in the input box, update it in the main window as well"
        self.__allowance = value
    
    def modelTypeChanged(self, value):
        "When the chute model changes in the input box, update it in the main window as well"
        self.__model_type = value
        self.updateDefaultFilename()

    def unitsChanged(self, value):
        "When the units change in the input box, update them in the main window as well"
        if value == "Centimeters":
            self.__units = 5
        else:
            self.__units = 1
    
    def folderChanged(self, value):
        "When the output folder changes in the input box, update it in the main window as well"
        self.__folder = value
    
    def folderButtonClicked(self):
        "Displays the dialog box to choose an output folder"
        self.optionsPane().folderBox().box().setText(str(QFileDialog.getExistingDirectory(self, "Select Folder")))
    
    def filenameChanged(self, value):
        "When the filename changes in the input box, update it in the main window as well"
        if value == "":
            self.updateDefaultFilename()
        else:
            self.__filename = value

    def updateButtonClicked(self):
        "Calculates and plots the gore outline and the outline with hem allowance"

        # Create an array to contain the chute profile points
        chute_profile = array(None)

        # Generate a chute profile based on the current profile type
        if self.profile() == 0:
            chute_profile = ellipticalPointList(self.diameter(), self.heightRatio(), self.innerDiameter())
        else:
            chute_profile = toroidalPointList(self.diameter(), self.innerDiameter(), self.heightRatio(), self.pulldownRatio())
        
        # Update the current gore profile based on the chute profile. Calculate the new gore profile with hem allowance and update the offset gore profile
        self.setPointList(goreProfile(chute_profile, self.numGores(), self.modelType()))
        self.setOffsetPointList(offset(self.pointList(), self.allowance()))

        # Plot the gore profile
        self.plot().clear()
        pen1 = pyqtgraph.mkPen(color="#000000", width=1, style=QtCore.Qt.SolidLine) # Style the gore profile line
        ptlst = array(self.pointList()) # Make the point list into an array
        ptlst.resize(len(ptlst)+1,2)    # Reshape the array to a list of 2D points
        ptlst[-1,:] = ptlst[0,:]    # Duplicate the first point to the end of the list
        self.plot().plot(ptlst[:,0], ptlst[:,1], pen=pen1)  # Plot the gore profile
        pen2 = pyqtgraph.mkPen(color="#FF0000", width=1, style=QtCore.Qt.DashLine)  # Style the offset profile pen
        offptlst = array(self.offsetPointList())    # Make the offset list into an array
        offptlst.resize(len(offptlst)+1, 2) # Reshape the array to a list of 2D points
        offptlst[-1,:] = offptlst[0,:]  # Duplicate the first point to the end of the list
        self.plot().plot(offptlst[:,0], offptlst[:,1], pen=pen2)    # Plot the offset profile
    
    def getDXFButtonClicked(self):
        "Clicks the update button, then outputs a dxf file of the gore template"
        self.updateButtonClicked()
        output = self.filename() + ".dxf"
        getDXF(self.offsetPointList(), self.folder().replace("\\","\\\\"), output, self.units())
    
    def updateDefaultFilename(self):
        "Sets the default filename based on the chute parameters and updates the filename box background text to match. If the filename box is empty, sets the filename to the default filename. Trigger this whenever an option changes that affects the default filename"
        if self.optionsPane().filenameBox().box().text() == "":
            self.__filename = "{:.0f}".format(self.diameter()) + "{:02.0f}".format(self.innerDiameter()) + "-" + str(self.numGores()) + chute_profile[self.profile()] + chute_type[self.modelType()]
        self.optionsPane().filenameBox().box().setPlaceholderText(self.filename())
