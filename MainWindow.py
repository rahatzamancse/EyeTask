import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from zeep import Client

from Speach import Speach
from WheelChair import WheelChair
from image_processors.BlinkDetector import BlinkDetector
from image_processors.FaceDetector import FaceDetector
from image_processors.GazeDetector import GazeDetector


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./ui/MainWindow.ui", self)
        self.setWindowTitle("Eye Based Wheelchair Control & Task Manager")
        self.resetButton.clicked.connect(self.resetAll)

        self.faceDetector = FaceDetector()

        self.currentFocus = 0
        self.__initialize_buttons()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.soundThread = None

        self.chair = WheelChair()

        self.current_subprecess = None

        # mode 0 = not controlling wheel chair; controlling menu with eye-blink
        # mode 1 = controling wheel chair with eye-gaze and eye-blink
        # mode 2 = Speech mode
        # mode 3 = Face mode
        # mode 4 = Face mode wheel chair
        self.current_mode = 0

        self.cap = cv2.VideoCapture(0)

        self.gazeDetector = GazeDetector()

        self.blinkDetector = BlinkDetector()

        self.speech = Speach()
        self.initialize_speech()

        self.timer.start(10)

        self.main_image_label.setScaledContents(True)

    def resetAll(self):
        self.current_mode = 0
        self.chair.stop()
        self.chair.is_going = False
        self.gazeDetector.reset()
        self.blinkDetector.reset()

    def updateFrame(self):
        #print(self.current_mode)
	
        info = {}
        if self.current_mode == 0 or self.current_mode == 1 or self.current_mode == 3 or self.current_mode == 4:
            _, img = self.cap.read()
            blink_dict = self.blinkDetector.run_blink_detector(img, self.eyeThreshold.value())
            if self.current_mode != 4 or self.current_mode != 2:
                outImage = toQImage(blink_dict["image"])
                outImage = outImage.rgbSwapped()
                self.main_image_label.setPixmap(QPixmap.fromImage(outImage))
            info["left"] = blink_dict["leftTotal"]
            info["right"] = blink_dict["rightTotal"]
            info["both"] = blink_dict["bothTotal"]
            info["rightEAR"] = blink_dict["rightEAR"]
            info["leftEAR"] = blink_dict["leftEAR"]
            info["avgEAR"] = (blink_dict["rightEAR"] + blink_dict["leftEAR"]) / 2
            flag = 0
            if blink_dict["both"]:
                if self.current_subprecess is not None:
                    self.current_subprecess.terminate()
                    self.current_subprecess = None
                    flag = 1
            if self.current_subprecess is not None:
                return
            if self.current_mode is 0:
                if blink_dict["left"]:
                    self.moveFocusLeft()
                if blink_dict["right"]:
                    self.moveFocusRight()
                if blink_dict["both"] and flag == 0:
                    self.pressFocused()

            elif self.current_mode is 1:
                gazeDict = self.gazeDetector.get_processed_image(img)
                info["dir"] = gazeDict["direction"]
                if gazeDict["direction"] == "left":
                    self.chair.left()
                if gazeDict["direction"] == "right":
                    self.chair.right()
                if gazeDict["direction"] == "center":
                    self.chair.start()

                if blink_dict["left"] or blink_dict["right"]:
                    self.chair.toggleStartStop()

                elif blink_dict["both"]:
                    self.chair.stop()
                    self.chair.is_going = False
                    self.current_mode = 0
                    self.gazeDetector.closeAll()

            elif self.current_mode == 3:
                faceDict = self.faceDetector.get_processed_image(img)
                if blink_dict["right"]:
                    self.faceDetector.initPos(faceDict["face"])

                if blink_dict["both"] and flag == 0:
                    self.pressFocused()

                if faceDict["direction"] == "right":
                    self.moveFocusRight()
                if faceDict["direction"] == "left":
                    self.moveFocusLeft()
                if faceDict["direction"] == "up":
                    self.moveFocusUp()
                if faceDict["direction"] == "down":
                    self.moveFocusDown()

            elif self.current_mode == 4:
                self.chair.is_going = True
                faceDict = self.faceDetector.get_processed_image(img)
                self.main_image_label.setText("Chair wheel Mode"
                                              "\n\n Press right eye to initialize"
                                              "\n\n Press both eye for exit")
                if blink_dict["both"]:
                    self.chair.stop()
                    self.chair.is_going = False
                    self.current_mode = 3

                if faceDict["direction"] == "right":
                    self.chair.right()
                elif faceDict["direction"] == "left":
                    self.chair.left()
                elif faceDict["direction"] == "up":
                    self.chair.start()
                elif faceDict["direction"] == "down":
                    self.chair.stop()
                elif faceDict["direction"] == "center":
                     self.chair.stop()

        elif self.current_mode == 2:
            if self.soundThread is None or not self.soundThread.is_alive():
                self.soundThread = Thread(target=self.speech.recognize_speech_from_mic)
                self.soundThread.start()
                print("Started Listening")
            self.main_image_label.setText("Listening")

        self.updateImageInfo(info)

    def updateImageInfo(self, dict):
        val = ""
        for key, value in dict.items():
            val = val + "\n" + str(key) + " : " + str(value)

        self.image_info_textlabel.setText(val)

    def initialize_speech(self):
        self.speech.commands["video"].append(self.playVideo)
        self.speech.commands["music"].append(self.playMusic)
        self.speech.commands["SMS"].append(self.playSMS)
        self.speech.commands["message"].append(self.playEmail)
        self.speech.commands["light"].append(self.playLight)
        self.speech.commands["ceiling fan"].append(self.playFan)
        self.speech.commands["news"].append(self.playBrowser)

        self.speech.commands["start"].append(self.chair.start)
        self.speech.commands["stop"].append(self.chair.stop)
        self.speech.commands["right"].append(self.chair.right)
        self.speech.commands["left"].append(self.chair.left)

        self.speech.commands["close"].append(self.stopCurrentSubprocess)


    def stopCurrentSubprocess(self):
        if self.current_subprecess is not None:
            self.current_subprecess.terminate()

    def comboboxIndexChanged(self):
        if self.selectMethodComboBox.currentIndex() == 0:
            self.current_mode = 0
        elif self.selectMethodComboBox.currentIndex() == 1:
            self.current_mode = 3
            self.chair.is_going = False
        elif self.selectMethodComboBox.currentIndex() == 2:
            self.current_mode = 2
            self.chair.is_going = True
        if self.selectMethodComboBox.currentIndex() != 2:
            self.soundThread = None

    def __initialize_buttons(self):
        self.selectMethodComboBox.clear()
        self.selectMethodComboBox.addItems([
            "Eye-Help",
            "Head-Help",
            "Voice-Help"
        ])
        self.selectMethodComboBox.setCurrentIndex(0)
        self.selectMethodComboBox.currentIndexChanged.connect(self.comboboxIndexChanged)

        self.buttons = [self.b1_1, self.b1_2,
                        self.b1_3, self.b2_1,
                        self.b2_2, self.b2_3,
                        self.b3_1, self.b3_2]
        for b in self.buttons:
            b.setAutoDefault(True)
        self.buttons[self.currentFocus].setFocus(True)

        self.b1_1.clicked.connect(self.controlWheel)
        self.b1_2.clicked.connect(self.playSMS)
        self.b1_3.clicked.connect(self.playEmail)
        self.b2_1.clicked.connect(self.playVideo)
        self.b2_2.clicked.connect(self.playMusic)
        self.b2_3.clicked.connect(self.playBrowser)
        self.b3_1.clicked.connect(self.playLight)
        self.b3_2.clicked.connect(self.playFan)

    def playSMS(self):
        try:
            url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
            client = Client(url)
            userName = '01521313223'
            password = '90053'
            recipientNumber = '01521323429'
            smsText = 'Help Me'
            smsType = 'TEXT'
            maskName = ''
            campaignName = ''
            client.service.OneToOne(userName, password, recipientNumber, smsText, smsType, maskName, campaignName)
            print('SMS sent!')
        except Exception as e:
            print('SMS nor sent!')
            print(e)

    def controlWheel(self):
        if self.current_mode == 3 or self.current_mode == 4:
            self.current_mode = 4
        else:
            self.current_mode = 1

    def playEmail(self):
        try:
            fromaddr = 'eyegaze.kuet@gmail.com'
            toaddr = 'sakibreza1@gmail.com'
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = 'Doctor Appointment'

            body = 'I am facing problem.Please come to see me if you are free.'
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, '060701cse')
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print('Email Sent Successfully')
        except Exception as e:
            print('Email not sent')
            print(e)

    def playFan(self):
        print("playing Fan")
        self.chair.playFan()

    def playLight(self):
        print("playing Light")
        self.chair.playLight()

    def playBrowser(self):
        import webbrowser
        webbrowser.open_new_tab("http://epaperna.prothomalo.com/")

    def playMusic(self):
        import os, random, subprocess
        randomfile = random.choice(os.listdir("F:\\music\\"))
        file = "F:\\music\\" + randomfile
        self.current_subprecess = subprocess.Popen(["C:\Program Files\Windows Media Player\wmplayer.exe", file])

    def playVideo(self):
        import os, random, subprocess
        randomfile = random.choice(os.listdir("F:\\video\\"))
        file = "F:\\video\\" + randomfile
        self.current_subprecess = subprocess.Popen(["C:\Program Files\Windows Media Player\wmplayer.exe", file])

    def moveFocusRight(self):
        if self.current_subprecess is None and self.current_mode != 1 and self.current_mode != 4:
            self.currentFocus = (self.currentFocus + 1) % 8
            self.buttons[self.currentFocus].setFocus(True)

    def moveFocusLeft(self):
        if self.current_subprecess is None and self.current_mode != 1 and self.current_mode != 4:
            self.currentFocus = (self.currentFocus - 1) % 8
            self.buttons[self.currentFocus].setFocus(True)

    def moveFocusUp(self):
        if  self.current_subprecess is None and self.current_mode != 1 and self.current_mode != 4:
            self.currentFocus = (self.currentFocus + 2) % 8
            self.buttons[self.currentFocus].setFocus(True)

    def moveFocusDown(self):
        if  self.current_subprecess is None and self.current_mode != 1 and self.current_mode != 4:
            self.currentFocus = (self.currentFocus - 2) % 8
            self.buttons[self.currentFocus].setFocus(True)

    def pressFocused(self):
        if self.current_subprecess is None and self.current_mode != 1 and self.current_mode != 4:
            self.buttons[self.currentFocus].animateClick()


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
