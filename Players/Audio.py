import fnmatch
import os

from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QColor, QFont)
from PyQt5.QtWidgets import QListView

from Resources.ResourceMusic import ResourceMusic


class Audio:
    def __init__(self):
        self.mediaLength = 0
        self.mediaList = []
        self.formats = ['*.mp3', '*.ogg']
        self.playing = False
        self.initUI()

    def togglePlay(self):
        
        if len(self.mediaList) != 0:
        
            if self.playing:
                self.pause()
                self.playing = False
            else:
                self.play()
                self.playing = True

    def initUI(self):
        self.list = QListView()
        self.list.setWindowTitle("Music Files")
        self.list.setMinimumSize(300, 400)
        self.list.setSpacing(10)
        self.model = QStandardItemModel(self.list)
        self.resourceMusic = ResourceMusic()

        for root, dirs, files in os.walk("MusicFiles"):
            for extensions in self.formats:
                for filename in fnmatch.filter(files, extensions):
                    item = QStandardItem(filename)
                    item.setFont(QFont(filename, 10))
                    self.model.appendRow(item)
                    self.mediaList.append(item)

        self.mediaLength = len(self.mediaList)
        self.currentItem = 1
        self.prevItem = self.mediaLength
        
        if len(self.mediaList) != 0:
            self.mediaList[0].setBackground(QColor(97, 138, 204))
            
        self.list.setModel(self.model)
        self.list.show()

    def nextItem(self):
        
        if len(self.mediaList) != 0:
        
            if self.currentItem == self.mediaLength:
                self.prevItem = self.mediaLength
                self.currentItem = 1
    
            else:
                self.prevItem = self.currentItem
                self.currentItem = self.currentItem + 1
    
            self.mediaList[self.prevItem - 1].setBackground(QColor(35, 38, 41))
            self.mediaList[self.currentItem - 1].setBackground(QColor(97, 138, 204))

    def play(self):
        print("Music Player : " + str(self.mediaList[self.currentItem - 1].text()))
        self.resourceMusic.playMusic(self.mediaList[self.currentItem - 1].text())
        return 1

    def pause(self):
        self.resourceMusic.pauseMusic()

    def stop(self):
        
        if len(self.mediaList) != 0:
            self.resourceMusic.stopMusic()
            self.playing = False

    def Close(self):
        self.list.close()
        return -1
