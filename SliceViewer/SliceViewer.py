import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QSlider, QComboBox
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import random
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt



class SliceViewer(QDialog):
    
    def __init__(self, volume, parent=None):
        super(SliceViewer, self).__init__(parent)
        
        self.volume = volume
        self.time_size, self.inline_size, self.xline_size = self.volume.shape
        
        self.figure = Figure(figsize=(4, 15))
        self.canvas = FigureCanvas(self.figure)
        
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        self.control_vbox = QVBoxLayout()
        self.slider = QSlider()
        self.slider.valueChanged[int].connect(self.change_value)
        
        self.slider.setOrientation(Qt.Vertical)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.inline_size)
        
        
        self.combo = QComboBox(self)
        self.combo.addItem("INLINE")
        self.combo.addItem("XLINE")
        self.combo.addItem("TIME")
        self.combo.activated[str].connect(self.combo_changed)  
        self.slider_value_label = QLabel('') 
        
        self.control_vbox.addWidget(self.slider_value_label)
        self.control_vbox.addWidget(self.slider)
                
        
        self.mpl_vbox = QVBoxLayout()
        self.mpl_vbox.addWidget(self.canvas)
        self.mpl_vbox.addWidget(self.combo)
        self.mpl_vbox.addWidget(self.toolbar)
        
        
        
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addLayout(self.mpl_vbox)
        self.hbox_layout.addLayout(self.control_vbox)
        
        self.combo_changed('INLINE')
        self.setLayout(self.hbox_layout)
        
        
    def change_value(self, value):
        self.slider_value_label.setText(str(value))
        self.show_slice()
        
    def combo_changed(self, text):
        if text =='INLINE':
            self.show_type = 'INLINE'
            self.slider.setMaximum(self.inline_size)
            self.slider.setValue(self.inline_size//2)
        elif text == 'XLINE':
            self.show_type = 'XLINE'
            self.slider.setMaximum(self.xline_size)
            self.slider.setValue(self.xline_size//2)
        else:
            self.show_type = 'TIME'
            self.slider.setMaximum(self.time_size)
            self.slider.setValue(self.time_size//2)
        self.show_slice()
            
        
    def show_slice(self):
        self.figure.clear()
        if self.show_type == 'INLINE':
            to_show = self.volume[:, :, self.slider.value()]
        elif self.show_type == 'XLINE':
            to_show = self.volume[:, self.slider.value(), :]
        else:
            to_show = self.volume[self.slider.value(), :, :]
            
        self.slice_axs = self.figure.add_subplot(111)
        self.slice_axs.imshow(to_show, aspect='auto', cmap='seismic')
        self.canvas.draw()