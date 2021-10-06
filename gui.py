from PyQt5 import QtCore
from numpy import number
from pyqtgraph.widgets.PlotWidget import PlotWidget
from config import *
from functions import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout, QLabel, QPushButton, QSlider, QSpinBox, QVBoxLayout, QWidget
import sys
import ctypes
import pyqtgraph

pyqtgraph.setConfigOptions(background="w", foreground="k",antialias=True)

class DropdownBox(QWidget):

    def __init__(self, title: str, options: list[str]) -> None:
        super().__init__()
        
        self.__label = QLabel()
        self.__box = QComboBox()
        self.__value = ""

        self.label().setText(title)
        self.box().addItems(options)
        self.__setValue(options[0])

        layout = QHBoxLayout()
        layout.addWidget(self.label())
        layout.addWidget(self.box())
        self.setLayout(layout)

        self.box().currentTextChanged.connect(self.__setValue)

    def label(self):
        return self.__label
    
    def box(self):
        return self.__box
    
    def value(self):
        return self.__value
    
    def __setValue(self, value):
        self.__value = value

class SliderWithBox(QWidget):
    
    def __init__(self, title: str, min: int, max: int, step: float):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__slider = QSlider(Qt.Horizontal)
        self.__box = QSpinBox()

        self.label().setText(title)
        self.slider().setRange(min, max)
        self.slider().setSingleStep(step)
        self.box().setMinimum(min)
        self.box().setValue(self.slider().value())

        self.layout().addWidget(self.label())
        layout = QHBoxLayout()
        layout.addWidget(self.slider())
        layout.addWidget(self.box())
        self.layout().addLayout(layout)

        self.slider().valueChanged.connect(self.sliderValueChanged)
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
        self.slider().setValue(value)
        self.box().setValue(value)
    
    def sliderValueChanged(self):
        self.box().setValue(self.slider().value())
        if self.label().text() == "Number of Gores":
            GUI_NUM_GORES = self.box().value()
    
    def boxValueChanged(self):
        self.slider().setValue(self.box().value())
        if self.label().text() == "Number of Gores":
            GUI_NUM_GORES = self.box().value()

class SliderWithDoubleBox(QWidget):
    
    def __init__(self, title: str, min: int, max: int, step: float):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.__label = QLabel()
        self.__slider = QSlider(Qt.Horizontal)
        self.__box = QDoubleSpinBox()

        self.label().setText(title)
        self.slider().setRange(min, max)
        self.slider().setSingleStep(step)
        self.box().setMinimum(min)
        self.box().setValue(self.slider().value())

        self.layout().addWidget(self.label())
        layout = QHBoxLayout()
        layout.addWidget(self.slider())
        layout.addWidget(self.box())
        self.layout().addLayout(layout)

        self.slider().valueChanged.connect(self.sliderValueChanged)
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
        self.slider().setValue(value)
        self.box().setValue(value)
    
    def sliderValueChanged(self):
        self.box().setValue(self.slider().value())
    
    def boxValueChanged(self):
        self.slider().setValue(self.box().value())

class AllowanceBox(QDoubleSpinBox):

    def __init__(self, min: float):
        super().__init__()
        self.setMinimum(min)
        self.setSingleStep(0.05)

class UpdateButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.setText("Plot gore")
       
class GetDXFButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.setText("Get DXF")

class OptionsPane(QWidget):

    def __init__(self):
        super().__init__()

        self.__chute_profile_dropdown = DropdownBox("Chute Profile", ["Elliptical", "Toroidal"])
        self.__diameter_slider = SliderWithDoubleBox("Diameter", 6, 96, 2)
        self.__inner_diameter_slider = SliderWithDoubleBox("Inner Diameter", 0, self.diameterSlider().value()/2, 1)
        self.__num_gores_slider = SliderWithBox("Number of Gores", 4, 12, 1)
        self.__allowance_box = AllowanceBox(0)
        self.__model_type_dropdown = DropdownBox("Model Type", ["Polygonal", "Circular"])
        self.__update_button = UpdateButton()
        self.__get_dxf_button = GetDXFButton()

        self.chuteProfileDropdown().box().setCurrentIndex(int(PROFILE))
        self.diameterSlider().setValue(float(DIAMETER))
        self.innerDiameterSlider().setValue(float(INNER_DIAMETER))
        self.numGoresSlider().setValue(int(NUM_GORES))
        self.allowanceBox().setValue(float(ALLOWANCE))

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.chuteProfileDropdown())
        layout.addWidget(self.diameterSlider())
        layout.addWidget(self.innerDiameterSlider())
        layout.addWidget(self.numGoresSlider())
        layout.addWidget(self.allowanceBox())
        layout.addWidget(self.modelTypeDropdown())
        layout.addWidget(self.updateButton())
        layout.addWidget(self.getDXFButton())
    
    def chuteProfileDropdown(self):
        return self.__chute_profile_dropdown

    def diameterSlider(self):
        return self.__diameter_slider
    
    def innerDiameterSlider(self):
        return self.__inner_diameter_slider
    
    def numGoresSlider(self):
        return self.__num_gores_slider
    
    def allowanceBox(self):
        return self.__allowance_box
    
    def modelTypeDropdown(self):
        return self.__model_type_dropdown
    
    def updateButton(self):
        return self.__update_button
    
    def getDXFButton(self):
        return self.__get_dxf_button

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        size = min(ctypes.windll.user32.GetSystemMetrics(0) / 16, ctypes.windll.user32.GetSystemMetrics(1) / 9)
        width = int(size * 4)
        height = int(size * 9 / 4)
        self.resize(width, height)
        self.setLayout(QHBoxLayout())

        self.__options_pane = OptionsPane()
        self.__plot = PlotWidget()

        self.layout().addWidget(self.optionsPane())
        self.layout().addWidget(self.plot())
        
        self.__profile = int(PROFILE)
        self.__diameter = float(DIAMETER)
        self.__inner_diameter = float(INNER_DIAMETER)
        self.__num_gores = int(NUM_GORES)
        self.__allowance = float(ALLOWANCE)
        self.__model_type = int(MODEL_TYPE)
        self.__units = int(UNITS)
        self.__point_list = array(None)
        self.__offset_point_list = array(None)

        self.optionsPane().chuteProfileDropdown().box().currentIndexChanged.connect(self.profileChanged)
        self.optionsPane().diameterSlider().box().valueChanged.connect(self.diameterChanged)
        self.optionsPane().innerDiameterSlider().box().valueChanged.connect(self.innerDiameterChanged)
        self.optionsPane().numGoresSlider().box().valueChanged.connect(self.numGoresChanged)
        self.optionsPane().allowanceBox().valueChanged.connect(self.allowanceChanged)
        self.optionsPane().modelTypeDropdown().box().currentIndexChanged.connect(self.modelTypeChanged)
        self.optionsPane().updateButton().clicked.connect(self.updateButtonClicked)
        self.optionsPane().getDXFButton().clicked.connect(self.getDXFButtonClicked)
    
    def optionsPane(self):
        return self.__options_pane
    
    def plot(self):
        return self.__plot
    
    def setPlot(self, plot):
        self.__plot = plot
    
    def profile(self):
        return self.__profile
    
    def diameter(self):
        return self.__diameter
    
    def innerDiameter(self):
        return self.__inner_diameter
    
    def numGores(self):
        return self.__num_gores
    
    def allowance(self):
        return self.__allowance
    
    def modelType(self):
        return self.__model_type
    
    def units(self):
        return self.__units
    
    def pointList(self):
        return self.__point_list
    
    def setPointList(self, list: ndarray):
        self.__point_list = list
    
    def offsetPointList(self):
        return self.__offset_point_list
    
    def setOffsetPointList(self, list):
        self.__offset_point_list = list
    
    def profileChanged(self):
        self.__profile = self.optionsPane().chuteProfileDropdown().box().currentIndex()
    
    def diameterChanged(self):
        self.__diameter = self.optionsPane().diameterSlider().value()
    
    def innerDiameterChanged(self):
        self.__inner_diameter = self.optionsPane().innerDiameterSlider().value()
    
    def numGoresChanged(self):
        self.__num_gores = self.optionsPane().numGoresSlider().value()
    
    def allowanceChanged(self):
        self.__allowance = self.optionsPane().allowanceBox().value()
    
    def modelTypeChanged(self):
        self.__model_type = self.optionsPane().modelTypeDropdown().box().currentIndex()
    
    def updateButtonClicked(self):
        chute_profile = array(None)
        if self.profile() == 0:
            chute_profile = ellipticalPointList(self.diameter(), RATIO, self.innerDiameter())
        else:
            chute_profile = toroidalPointList(self.diameter(), self.innerDiameter(), RATIO)
        self.setPointList(goreProfile(chute_profile, self.numGores(), self.modelType()))
        self.setOffsetPointList(offset(self.pointList(), self.allowance()))
        self.setPlot(PlotWidget())
        self.plot().plot(self.pointList()[:,0], self.pointList()[:,1], pen=pyqtgraph.mkPen(color="#000000", width=1, style=QtCore.Qt.SolidLine))
        self.plot().plot(self.offsetPointList()[:,0], self.offsetPointList()[:,1], pen=pyqtgraph.mkPen(color="#FF0000", width=1, style=QtCore.Qt.DashLine))
    
    def getDXFButtonClicked(self):
        output = chute_profile[self.profile()] + str(round(self.diameter(), 3)) + "x" + str(self.numGores()) + chute_type[self.modelType()] + "_" + str(round(RATIO, 3)) + "_" + str(round(self.allowance(),3)) + "_" + str(round(self.innerDiameter())) + "_units" + str(self.units()) + ".dxf"
        getDXF(self.offsetPointList(), FOLDER, output, self.units())
