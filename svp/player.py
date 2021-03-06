#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2

class Player(QWidget):
    def __init__(self, *args):
        super(QWidget, self).__init__()
        # store displays
        self._displays = []
        # set openCV capture
        self.cap = cv2.VideoCapture(*args)
        self.filepath = args[0]
        self.timer = QTimer()
        self.timer.setInterval(1000./25)
        self.timer.timeout.connect(self.nextFrameSlot)


    def setFPS(self, fps):
        self.fps = fps

    def addDisplay(self, display):
        self._displays.append(display)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            #print(self.cap.get(2))
            if self._displays:
                for display in self._displays:
                    if display.available:
                        display.video_frame.setPixmap(pix)
        else:
            self.eject()

    def load(self, filepath):
        self.filepath = filepath
        self.cap.open(self.filepath)
        ret, frame = self.cap.read()
        if ret:
            if frame.any():
                #['CV_CAP_PROP_POS_MSEC','CV_CAP_PROP_POS_FRAMES','CV_CAP_PROP_POS_AVI_RATIO','CV_CAP_PROP_FRAME_WIDTH','CV_CAP_PROP_FRAME_HEIGHT','CV_CAP_PROP_FPS','CV_CAP_PROP_FOURCC','CV_CAP_PROP_FRAME_COUNT','CV_CAP_PROP_FORMAT','CV_CAP_PROP_MODE','CV_CAP_PROP_CONVERT_RGB','CV_CAP_PROP_WHITE_BALANCE_U','CV_CAP_PROP_WHITE_BALANCE_V','CV_CAP_PROP_BUFFERSIZE']
                self.width = self.cap.get(3)
                self.height = self.cap.get(4)
                self.fps = self.cap.get(5)
                self.timer.setInterval(1000./self.fps)
                print(self.filepath, self.fps, self.width, self.height)
        self.start()

    def start(self):
        self.timer.start()

    def pause(self):
        self.timer.stop()
    
    def resume(self, state):
        self.timer.start()

    def eject(self):
        self.cap.release()
        self.timer.stop()
        for display in self._displays:
            if display.available:
                display.clear()
