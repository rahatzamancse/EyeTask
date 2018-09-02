import pyautogui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class ResourceKeyboard(QMainWindow):
    def __init__(self, fortask):
        super(ResourceKeyboard, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        loadUi("UI/Keyboard.ui", self)
        self.currentFocus = 11
        self.currentFloat = 0
        self.__initializeButtons()
        self.__initializeFloatButtons()
        self.__initializeKeys()
        self.show()
        self.keyEdit.setFocus()
        self.str = ""
        self.timer = QTimer(self)
        self.allow = True
        self.timer.timeout.connect(self.setAllow)
        self.timer.start(1000)
        self.fortask = fortask

    def setAllow(self):
        self.allow = True

    def __initializeButtons(self):
        self.buttons = [self.button_1, self.button_2, self.button_3,
                        self.button_4, self.button_5, self.button_6,
                        self.button_7, self.button_8, self.button_9, self.button_0,
                        self.button_Cancel, self.button_Done]

        for b in self.buttons:
            b.setAutoDefault(True)
            b.setStyleSheet("background-color: black")

        self.buttons[self.currentFocus].setStyleSheet("background-color: blue")
        
    def __initializeFloatButtons(self):
        self.floatButtons = {self.button_1: [self.button_Enter, self.button_Space],
                             self.button_2: [self.button_a, self.button_b, self.button_c],
                             self.button_3: [self.button_d, self.button_e, self.button_f],
                             self.button_4: [self.button_g, self.button_h, self.button_i],
                             self.button_5: [self.button_j, self.button_k, self.button_l],
                             self.button_6: [self.button_m, self.button_n, self.button_o],
                             self.button_7: [self.button_p, self.button_q, self.button_r, self.button_s],
                             self.button_8: [self.button_t, self.button_u, self.button_v],
                             self.button_9: [self.button_w, self.button_x, self.button_y, self.button_z],
                             self.button_0: [],
                             self.button_Cancel: [],
                             self.button_Done: []}

        for b in self.buttons:
            for floatButtons in self.floatButtons[b]:
                floatButtons.setAutoDefault(True)
                floatButtons.setStyleSheet("background-color: black")
                floatButtons.setVisible(False)

    def __initializeKeys(self):
        self.keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'backspace']
        self.floatKeys = {'1': ['enter', 'space'],
                          '2': ['a', 'b', 'c'],
                          '3': ['d', 'e', 'f'],
                          '4': ['g', 'h', 'i'],
                          '5': ['j', 'k', 'l'],
                          '6': ['m', 'n', 'o'],
                          '7': ['p', 'q', 'r', 's'],
                          '8': ['t', 'u', 'v'],
                          '9': ['w', 'x', 'y', 'z']}

    def moveFocusInitial(self):
        self.prevFocus = self.currentFocus
        self.currentFocus = 10

        for floatButtons in self.floatButtons[self.buttons[self.prevFocus]]:
            floatButtons.setStyleSheet("background-color: black")
            floatButtons.setVisible(False)

        for floatButtons in self.floatButtons[self.buttons[self.currentFocus]]:
            floatButtons.setVisible(True)

        self.currentFloat = 0
        self.buttons[self.prevFocus].setStyleSheet("background-color: black")
        self.buttons[self.currentFocus].setStyleSheet("background-color: blue")

    def moveFocusRight(self):

        self.prevFocus = self.currentFocus
        self.currentFocus = (self.currentFocus + 1) % len(self.buttons)

        for floatButtons in self.floatButtons[self.buttons[self.prevFocus]]:
            floatButtons.setStyleSheet("background-color: black")
            floatButtons.setVisible(False)

        for floatButtons in self.floatButtons[self.buttons[self.currentFocus]]:
            floatButtons.setVisible(True)

        self.currentFloat = 0
        self.buttons[self.prevFocus].setStyleSheet("background-color: black")
        self.buttons[self.currentFocus].setStyleSheet("background-color: blue")

    def moveFocusLeft(self):

        self.prevFocus = self.currentFocus
        self.currentFocus = (self.currentFocus - 1) % len(self.buttons)

        for floatButtons in self.floatButtons[self.buttons[self.prevFocus]]:
            floatButtons.setStyleSheet("background-color: black")
            floatButtons.setVisible(False)

        for floatButtons in self.floatButtons[self.buttons[self.currentFocus]]:
            floatButtons.setVisible(True)

        self.currentFloat = 0
        self.buttons[self.prevFocus].setStyleSheet("background-color: black")
        self.buttons[self.currentFocus].setStyleSheet("background-color: blue")

    def moveFloatRight(self):

        if self.allow:
            if (self.currentFocus != 9 and self.currentFocus != 10 and self.currentFocus != 11):

                self.prevFloat = self.currentFloat
                self.currentFloat = (self.currentFloat + 1) % (len(self.floatButtons[self.buttons[self.currentFocus]]) + 1)

                if (self.prevFloat == 0):
                    self.buttons[self.currentFocus].setStyleSheet("background-color: black")
                    self.floatButtons[self.buttons[self.currentFocus]][self.currentFloat - 1].setStyleSheet(
                        "background-color: blue")

                elif (self.currentFloat == 0):
                    self.buttons[self.currentFocus].setStyleSheet("background-color: blue")
                    self.floatButtons[self.buttons[self.currentFocus]][self.prevFloat - 1].setStyleSheet(
                        "background-color: black")

                else:
                    self.floatButtons[self.buttons[self.currentFocus]][self.prevFloat - 1].setStyleSheet(
                        "background-color: black")
                    self.floatButtons[self.buttons[self.currentFocus]][self.currentFloat - 1].setStyleSheet(
                        "background-color: blue")
            self.allow = False

    def moveFloatLeft(self):

        if self.allow:
            if self.currentFocus != 9 and self.currentFocus != 10 and self.currentFocus != 11:
                self.prevFloat = self.currentFloat
                self.currentFloat = (self.currentFloat - 1) % (len(self.floatButtons[self.buttons[self.currentFocus]]) + 1)

                if self.prevFloat == 0:
                    self.buttons[self.currentFocus].setStyleSheet("background-color: black")
                    self.floatButtons[self.buttons[self.currentFocus]][self.currentFloat - 1].setStyleSheet(
                        "background-color: blue")

                elif (self.currentFloat == 0):
                    self.buttons[self.currentFocus].setStyleSheet("background-color: blue")
                    self.floatButtons[self.buttons[self.currentFocus]][self.prevFloat - 1].setStyleSheet(
                        "background-color: black")

                else:
                    self.floatButtons[self.buttons[self.currentFocus]][self.prevFloat - 1].setStyleSheet(
                        "background-color: black")
                    self.floatButtons[self.buttons[self.currentFocus]][self.currentFloat - 1].setStyleSheet(
                        "background-color: blue")
            self.allow = False

    def selectKey(self):

        if self.currentFocus != 11:
            if self.currentFloat == 0:
                pyautogui.press(self.keys[self.currentFocus])
            else:
                pyautogui.press(self.floatKeys[self.keys[self.currentFocus]][self.currentFloat - 1])

            self.moveFocusInitial()
            return False

        else:
            self.str = self.keyEdit.text()
            self.close()
            return True
