# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:38:47 2024

@author: calvaresematteo
"""

'''Import useful python libraries'''
import os, sys
import numpy as np
'''Import GUI libraries'''
from qtpy import QtWidgets, uic
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
'''Import program modules'''
from device.webcam_device import WebcamDevice

class QtExampleApp(QtWidgets.QWidget):

    def __init__(self):
        '''Initialize the object'''

        # Initialize the parent class
        super().__init__()
        # Import the .ui UI and set it up
        self.import_ui()
        self.setup_ui()


    def import_ui(self):
        '''Import the .ui file created with Qt Designer'''

        # Get the ui file path name
        dir_path = os.path.dirname(__file__)
        form_file_path = 'ui\\form_example.ui'
        self.ui_filename = os.path.join(dir_path, form_file_path)

        # Import the ui file
        self.ui = uic.loadUi(self.ui_filename)
        

    def setup_ui(self):
        '''Set up the Qt widgets in the UI'''

        # Create and connect the image plot widget
        self.image_widget = pg.ImageView()
        self.ui.plot_groupBox.layout().addWidget(self.image_widget)

        # Set up the refresh rate spinbox 
        self.ui.spinBox.setValue(50)
        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setMaximum(100)

        # Connect the buttons
        self.ui.pushButton_start.clicked.connect(self.start_plotting)
        self.ui.pushButton_stop.clicked.connect(self.stop_plotting)
        self.ui.pushButton_reset.clicked.connect(self.reset_plot)

        # Set autolevels checbox to on
        self.ui.checkBox_autolevels.setChecked(True)

        # Set up the timer for the automatic update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)


    def start_plotting(self):
        '''Start function that runs when the start button is clicked'''

        # Read the refresh rate and calculate the refresh period
        self.refresh_rate = self.ui.spinBox.value()
        refresh_period = int(1000*1/(self.refresh_rate))

        # Disable the start button during acquisition
        self.ui.pushButton_start.setEnabled(False) 
        self.ui.pushButton_reset.setEnabled(False)  

        # Create connection to the camera
        self.camera = WebcamDevice()

        # Start the timer with the given refresh period
        self.timer.start(refresh_period)


    def update_image(self):
        '''Function that periodically updates the image plot, according to the timer'''

        # Update the image
        self.correct_frame, self.image = self.camera.acquire_image()
        self.image_widget.setImage(self.image,
                                autoLevels = self.ui.checkBox_autolevels.isChecked(),
                                autoRange = self.ui.checkBox_autorange.isChecked(),
                                levelMode = 'rgba')  
    
    def stop_plotting(self):
        '''Stop function that runs when the stop button is clicked'''

        # Stop the timer for the automatic update
        self.timer.stop()

        # Enable the start and reset buttons
        self.ui.pushButton_start.setEnabled(True)  
        self.ui.pushButton_reset.setEnabled(True)  

        # Close connection to the camera
        self.camera.close_connection()
 
    def reset_plot(self):
        '''Reset function that runs when the reset button is clicked'''

        # Set the image to zero and update the plot
        self.image = np.zeros((200, 200))
        self.image_widget.setImage(self.image,
                                autoLevels = self.ui.checkBox_autolevels.isChecked(),
                                autoRange = self.ui.checkBox_autorange.isChecked(),
                                levelMode = 'mono')  

      

if __name__ == "__main__":

    # Instantiate the application 
    app = QtWidgets.QApplication([])

    # Open the widget and set size and title of the UI
    widget = QtExampleApp()
    widget.ui.resize(1200, 900)
    widget.ui.setWindowTitle("Qt example app")
    widget.ui.show()

    # Execute the application
    sys.exit(app.exec())