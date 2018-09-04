import cv2
from PyQt5.QtGui import QImage, QPixmap

import MainWindow
from inputs.FaceDetector import FaceDetector
from inputs.GazeDetectorCnn import GazeDetector
from inputs.Speech import Speech


# Commands :
# left
# right
# up
# down
# press
# exit

class Controller:
    def __init__(self, main_window, giveOutput):
        self.gazeImg = None

        self.face_detector = FaceDetector()
        self.gaze_detector = GazeDetector()
        self.speech_detector = Speech()
        self.giveOutput = giveOutput
        self.main_window = main_window
        self.cap = cv2.VideoCapture(0)

        self.bothBlinkCounter = 0
        self.leftBlinkCounter = 0
        self.rightBlinkCounter = 0

        self.centerGazeCounter = 0
        self.leftGazeCounter = 0
        self.rightGazeCounter = 0

    def resetAllCounter(self):
        self.bothBlinkCounter = 0
        self.leftBlinkCounter = 0
        self.rightBlinkCounter = 0
        self.centerGazeCounter = 0
        self.leftGazeCounter = 0
        self.rightGazeCounter = 0

    def getInput(self):
        # Blink and Gaze
        _, img = self.cap.read()
        dicGaze = self.gaze_detector.processImage(img)

        blinkCounter = self.main_window.blink_counter_spinbox.value()
        gazeCounter = self.main_window.gaze_counter_spinbox.value()

        blink = dicGaze["blink"]
        if blink == "both":
            if self.bothBlinkCounter > blinkCounter:
                self.resetAllCounter()
                self.giveOutput("blinkboth")
                return
            else:
                x = self.bothBlinkCounter
                self.resetAllCounter()
                self.bothBlinkCounter = x + 1
        elif blink == "left":
            if self.leftBlinkCounter > blinkCounter:
                self.resetAllCounter()
                if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
                    self.face_detector.initPos()
                else:
                    self.giveOutput("blinkleft")
                return
            else:
                x = self.leftBlinkCounter
                self.resetAllCounter()
                self.leftBlinkCounter = x + 1
        elif blink == "right":
            if self.rightBlinkCounter > blinkCounter:
                self.resetAllCounter()
                self.giveOutput("blinkright")
                return
            else:
                x = self.rightBlinkCounter
                self.resetAllCounter()
                self.rightBlinkCounter = x + 1
        else:
            self.resetAllCounter()

        if dicGaze["gazeleft"] is not None:
            outImage = toQImage(dicGaze["gazeleft"])
            outImage = outImage.rgbSwapped()
            self.main_window.right_gaze_label.setPixmap(QPixmap.fromImage(outImage))

        if dicGaze["gazeright"] is not None:
            outImage = toQImage(dicGaze["gazeright"])
            outImage = outImage.rgbSwapped()
            self.main_window.left_gaze_label.setPixmap(QPixmap.fromImage(outImage))

        gazeDirection = dicGaze["gazedirection"]
        if gazeDirection != "gazenone":
            self.giveOutput(gazeDirection)

        drawImg = dicGaze["img"]
        dicHead = None
        if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
            dicHead = self.face_detector.processImage(img, drawImg)

        if dicHead is not None:
            if dicHead["direction"] != "not initialized":
                self.giveOutput(dicHead["direction"])

        outImage = toQImage(drawImg)
        outImage = outImage.rgbSwapped()
        self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))


def toQImage(raw_img):
    from numpy import copy
    img = copy(raw_img)
    qformat = QImage.Format_Indexed8
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    outImg = QImage(img.tobytes(), img.shape[1], img.shape[0], img.strides[0], qformat)
    return outImg
