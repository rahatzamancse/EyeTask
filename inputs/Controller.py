import cv2
from PyQt5.QtGui import QImage, QPixmap

import MainWindow
from inputs.BlinkDetector import BlinkDetector
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
        self.blink_detector = BlinkDetector()
        self.face_detector = FaceDetector()
        self.gaze_detector = GazeDetector()
        # self.speech_detector = Speech()
        self.giveOutput = giveOutput
        self.main_window = main_window
        self.cap = cv2.VideoCapture(0)

    def getInput(self):
        dicBlink = None
        dicGaze = None
        dicHead = None
        label = ""
        self.drawImg = None
        img = None

        # Blink
        if True:
            _, img = self.cap.read()
            dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())

            drawImg = dicBlink["img"]

            label = label + \
                    "Blink Detector : " + "\n" \
                                          "\t" + "both : " + str(dicBlink["both"]) + "\n" \
                                                                                     "\t" + "left : " + str(
                dicBlink["left"]) + "\n" \
                                    "\t" + "right : " + str(dicBlink["right"]) + "\n" \
                                                                                 "\t" + "leftEAR : " + str(
                dicBlink["leftEAR"]) + "\n" \
                                       "\t" + "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" \
                                                                                         "\t" + "bothTotal : " + str(
                dicBlink["bothTotal"]) + "\n" \
                                         "\t" + "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" \
                                                                                              "\t" + "rightTotal : " + str(
                dicBlink["rightTotal"]) + "\n" \
 \
                # Head
        if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
            dicHead = self.face_detector.processImage(img, drawImg)

            label = label + \
                    "Head Detector : " + "\n" \
                                         "\t" + "direction : " + str(dicHead["direction"]) + "\n"

        # GAZE
        if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.EYE_HELP \
                and self.main_window.current_mode in [MainWindow.MODE.CHAIR, MainWindow.MODE.KEYBOARD]:

            dicGaze = self.gaze_detector.processImage(img)

            label = label + \
                    "Gaze Detector : " + "\n" \
                                         "\t" + "Gaze : " + str(dicGaze["direction"]) + "\n"

            if dicGaze["img"] is not None:
                self.gazeImg = dicGaze["img"]
                self.gazeImg = toQImage(self.gazeImg)
                self.gazeImg = self.gazeImg.rgbSwapped()

            if self.gazeImg is not None:
                self.main_window.gaze_image_label.setPixmap(QPixmap.fromImage(self.gazeImg))
            else:
                self.main_window.gaze_image_label.setText("None")

        outImage = toQImage(drawImg)
        outImage = outImage.rgbSwapped()
        self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
        self.main_window.image_info_textlabel.setText(label)

        if dicBlink is not None:
            if dicBlink["left"]:
                if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
                    self.face_detector.initPos(dicHead["face"])
                    return
                self.giveOutput("blinkleft")
                return
            elif dicBlink["right"]:
                self.giveOutput("blinkright")
                return
            elif dicBlink["both"]:
                self.giveOutput("blinkboth")
                return

        if dicHead is not None:
            if dicHead["direction"] != "not initialized":
                self.giveOutput(dicHead["direction"])
                return

        if dicGaze is not None:
            if dicGaze["direction"] != "not initialized":
                self.giveOutput(dicGaze["direction"])
                return


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
