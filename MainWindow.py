from enum import IntEnum, auto

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QStatusBar
from PyQt5.uic import loadUi

from Resources.ResourceKeyboard import ResourceKeyboard
from WheelChair import WheelChair

from inputs.Controller import Controller
from Resources.ResourceKeyboard import ResourceKeyboard

class MODE(IntEnum):
    CHAIR = auto()
    MAIN = auto()
    SUBPROC = auto()
    AUDIO = auto()
    VIDEO = auto()
    NEWS = auto()
    PLAYING = auto()
    NEWSING = auto()
    SMS = auto()
    EMAIL = auto()
    KEYBOARD = auto()


class METHOD(IntEnum):
    EYE_HELP = 0
    HEAD_HELP = 1
    VOICE_HELP = 2


class MainWindow(QMainWindow):
    def __init__(self):
        WINDOW_TITLE = "Eye Based Wheelchair Control & Task Manager"
        GUI_UI_LOCATION = "./UI/MainWindow.ui"

        super(MainWindow, self).__init__()
        loadUi(GUI_UI_LOCATION, self)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome")

        self.setWindowTitle(WINDOW_TITLE)
        self.main_image_label.setScaledContents(True)
        self.gaze_image_label.setScaledContents(True)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.b = QtGui.QPushButton("exit", self, clicked=self.close)

        self.resetButton.clicked.connect(self.resetAll)

        self.chair = WheelChair()

        self.keyboard = None
        self.msg = ""

        self.current_mode = MODE.MAIN
        self.current_focus = 0

        self.__initialize_buttons()

        self.player = None
        self.document = None

        self.main_controller = Controller(self, self.gotInput)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main_controller.getInput)
        self.timer.start(100)

    def gotInput(self, command):
        print("Got input : " + str(command))

        if command == "not initialized":
            self.statusBar.showMessage("Please Initialize First")
            return

        if self.current_mode == MODE.MAIN:
            if command in ["blinkleft", "headleft"]:
                self.moveFocusLeft()
            elif command in ["blinkright", "headright"]:
                self.moveFocusRight()
            elif command in ["headup"]:
                self.moveFocusUp()
            elif command in ["headdown"]:
                self.moveFocusDown()
            elif command in ["blinkboth"]:
                self.pressFocused()

        elif self.current_mode == MODE.CHAIR:
            if command in ["gazeleft", "headleft"]:
                self.chair.left()
            elif command in ["gazeright", "headright"]:
                self.chair.right()
            elif command in ["blinkboth"]:
                self.chair.toggleStartStop()
            elif command in ["blinkleft", "blinkright"]:
                self.chair.active = False
                self.changeMode(MODE.MAIN)

        elif self.current_mode == MODE.AUDIO:
            if command in ["blinkright", "headright"]:
                self.player.nextItem()
            elif command in ["blinkleft", "headleft"]:
                self.statusBar.showMessage("Select an option...")
                if self.player.playing:
                    self.player.stop()
                else:
                    self.player.Close()
                    self.changeMode(MODE.MAIN)
            elif command == "blinkboth":
                self.player.togglePlay()
                
        elif self.current_mode == MODE.VIDEO:
            if command in ["blinkright","headright"]:
                self.player.nextItem()
            elif command in ["blinkleft","headleft"]:
                if self.player.resourceVideo.process != None:
                    self.player.stop()
                else:
                    self.player.Close()
                    self.changeMode(MODE.MAIN)
            elif command in ["blinkboth"]:
                self.player.togglePlay()

        elif self.current_mode == MODE.NEWS:
            if command in ["blinkright","headdown"]:
                self.document.nextItem()
            elif command in ["blinkleft","headleft"]:
                self.document.destroy()
                self.changeMode(MODE.MAIN)
            elif command in ["blinkboth"]:
                if self.document.Open():
                    self.changeMode(MODE.NEWSING)

        elif self.current_mode == MODE.NEWSING:
            if command in ["binkright","headright"]:
                self.document.scrollDown()
            elif command in ["blinkleft","headleft"]:
                self.document.scrollUp()
            elif command in ["blinkboth"]:
                self.document.Close()
                self.changeMode(MODE.NEWS)

        elif self.current_mode is MODE.KEYBOARD:
            if self.selectMethodComboBox.currentIndex() == METHOD.EYE_HELP:
                if command in ["blinkright"]:
                    self.keyboard.moveFocusRight()
                elif command in ["blinkleft"]:
                    self.keyboard.moveFocusLeft()
                if command in ["gazeright"]:
                    self.keyboard.moveFloatRight()
                elif command in ["gazeleft"]:
                    self.keyboard.moveFloatLeft()

            elif self.selectMethodComboBox.currentIndex() == METHOD.HEAD_HELP:
                if command in ["headright"]:
                    self.keyboard.moveFocusRight()
                elif command in ["headleft"]:
                    self.keyboard.moveFocusLeft()
                if command in ["blinkright"]:
                    self.keyboard.moveFloatRight()
                elif command in ["blinkleft"]:
                    self.keyboard.moveFloatLeft()

            if command in ["blinkboth"]:
                if self.keyboard.selectKey():
                    self.msg = self.keyboard.str
                    nxtMode = self.keyboard.fortask
                    self.keyboard = None
                    if nxtMode == "sms":
                        self.changeMode(MODE.SMS)
                    elif nxtMode == "email":
                        self.changeMode(MODE.EMAIL)


        elif self.current_mode == MODE.SMS:
            from zeep import Client
            try:
                url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
                client = Client(url)
                userName = '01521313223'
                password = '90053'
                recipientNumber = '01521323429'
                smsText = self.msg
                smsType = 'TEXT'
                maskName = ''
                campaignName = ''
                client.service.OneToOne(userName, password, recipientNumber, smsText, smsType, maskName,
                                        campaignName)
                self.statusBar.showMessage("SMS sent!!")
            except Exception as e:
                self.statusBar.showMessage("SMS not sent!!")
                print(e)

            self.changeMode(MODE.MAIN)
            
        elif self.current_mode == MODE.EMAIL:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            import smtplib
            try:
                fromaddr = 'eyegaze.kuet@gmail.com'
                toaddr = 'sakibreza1@gmail.com'
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = 'Doctor Appointment'
    
                body = self.msg
                msg.attach(MIMEText(body, 'plain'))
    
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, '060701cse')
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                self.statusBar.showMessage("Email sent")
                server.quit()
            except Exception as e:
                self.statusBar.showMessage("Email not sent")
                print(e)
                
            self.changeMode(MODE.MAIN)

    def closeEvent(self, event):
        # self.main_controller.closed()
        # self.deleteLater()
        pass

    def resetAll(self):
        pass

    def __initialize_buttons(self):
        self.selectMethodComboBox.clear()
        self.selectMethodComboBox.addItems([
            "Eye-Help",
            "Head-Help",
            "Voice-Help"
        ])
        self.selectMethodComboBox.setCurrentIndex(METHOD.EYE_HELP)
        self.selectMethodComboBox.currentIndexChanged.connect(self.comboboxIndexChanged)

        self.buttons = [self.b1_1, self.b1_2,
                        self.b1_3, self.b2_1,
                        self.b2_2, self.b2_3,
                        self.b3_1, self.b3_2]
        for b in self.buttons:
            b.setAutoDefault(True)
        self.buttons[self.current_focus].setFocus(True)

        self.b1_1.clicked.connect(self.controlWheel)
        self.b1_2.clicked.connect(self.playSMS)
        self.b1_3.clicked.connect(self.playEmail)
        self.b2_1.clicked.connect(self.playVideo)
        self.b2_2.clicked.connect(self.playMusic)
        self.b2_3.clicked.connect(self.playDocument)
        self.b3_1.clicked.connect(self.playLight)
        self.b3_2.clicked.connect(self.playFan)

    def comboboxIndexChanged(self):
        import cv2
        cv2.destroyAllWindows()
        # TODO
        if self.selectMethodComboBox.currentIndex() == METHOD.EYE_HELP:
            pass
        elif self.selectMethodComboBox.currentIndex() == METHOD.HEAD_HELP:
            pass
        elif self.selectMethodComboBox.currentIndex() == METHOD.VOICE_HELP:
            pass

    def moveFocusRight(self):
        if self.current_mode is MODE.MAIN:
            self.current_focus = (self.current_focus + 1) % 8
            self.buttons[self.current_focus].setFocus(True)

    def moveFocusLeft(self):
        self.current_focus = (self.current_focus - 1) % 8
        self.buttons[self.current_focus].setFocus(True)

    def moveFocusUp(self):
        self.current_focus = (self.current_focus - 2) % 8
        self.buttons[self.current_focus].setFocus(True)

    def moveFocusDown(self):
        self.current_focus = (self.current_focus + 2) % 8
        self.buttons[self.current_focus].setFocus(True)

    def pressFocused(self):
        self.buttons[self.current_focus].animateClick()
        
    def playFan(self):
        self.chair.toggleFan()
     
    def controlWheel(self):
        self.chair.active = True
        self.changeMode(MODE.CHAIR)

    def moveWindow(self, left, top):
        from PyQt5 import QtWidgets
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        height = sizeObject.height()
        width = sizeObject.width()
        self.move(int(width * left), int(height * top))

    def playFan(self):
        self.chair.toggleFan()

    def playLight(self):
        self.chair.toggleLight()

    def playMusic(self):
        from Players.Audio import Audio
        self.changeMode(MODE.AUDIO)
        self.player = Audio()

    def playVideo(self):
        from Players.Video import Video
        self.changeMode(MODE.VIDEO)
        self.player = Video()

    def playSMS(self):
        self.keyboard = ResourceKeyboard("sms")
        self.changeMode(MODE.KEYBOARD)

    def playEmail(self):
        
        self.keyboard = ResourceKeyboard("email")
        self.changeMode(MODE.KEYBOARD)

    def playDocument(self):
        from Document import Document
        self.changeMode(MODE.NEWS)
        self.document = Document()

    def changeMode(self, mode):
        self.current_mode = mode
        if mode is MODE.KEYBOARD:
            self.statusBar.showMessage("Please type what you want")
        elif mode is MODE.SMS:
            self.statusBar.showMessage("Sending sms")
        elif mode is MODE.CHAIR:
            self.statusBar.showMessage("Wheelchair control mode")
        elif mode is MODE.NEWSING:
            self.statusBar.showMessage("Reading PDF")
        elif mode is MODE.AUDIO:
            self.statusBar.showMessage("Playing Audio")
        elif mode is MODE.SUBPROC:
            self.statusBar.showMessage("In subprocess mode")
        elif mode is MODE.MAIN:
            self.statusBar.showMessage("Please Select an option")
            self.gaze_image_label.setText("Not using Eye gaze")
