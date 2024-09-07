# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:21:08 2024

@author: calvaresematteo
"""

'''Import useful python libraries'''
import cv2
import numpy as np

class WebcamDevice():

    def __init__(self):

        try:
            # Initialize the camera
            self.webcam = cv2.VideoCapture(0)   # 0 -> index of camera
            print('Connection to the webcam successfully created')
        except: 
            print('Connection to the webcam unsuccessful')
        
        
    
    def acquire_image(self):
        
        # Acquire a frame
        correct_frame, frame = self.webcam.read()
        frame = np.rot90(frame)

        return correct_frame, frame
    
    def close_connection(self):

        # Release the camera connection
        self.webcam.release()


