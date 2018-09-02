#import fnmatch
#import os
#
#from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QColor, QFont)
#from PyQt5.QtWidgets import QListView

from Resources.ResourceBrowser import ResourceBrowser


class Browser:
    def __init__(self,address):
        self.webAddress = address
        self.resourceBrowser = ResourceBrowser()
        self.Open()
        
#    def destroy(self):
#        self.list.close()
#        return -1

#    def initUI(self):
#        self.list = QListView()
#        self.list.setWindowTitle("Documents")
#        self.list.setMinimumSize(300, 400)
#        self.list.setSpacing(10)
#        self.model = QStandardItemModel(self.list)
#        self.resourcePdf = ResourcePdf()
#
#        for root, dirs, files in os.walk("Documents"):
#            for extensions in self.formats:
#                for filename in fnmatch.filter(files, extensions):
#                    item = QStandardItem(filename)
#                    item.setFont(QFont(filename, 10))
#                    self.model.appendRow(item)
#                    self.docList.append(item)
#
#        self.docLength = len(self.docList)
#        self.currentItem = 1
#        self.prevItem = self.docLength
#        if len(self.docList) != 0:
#            self.docList[0].setBackground(QColor(97, 138, 204))
#        self.list.setModel(self.model)
#        self.list.show()

#    def nextItem(self):
#        if len(self.docList) != 0:
#            if self.currentItem == self.docLength:
#                self.prevItem = self.docLength
#                self.currentItem = 1
#            else:
#                self.prevItem = self.currentItem
#                self.currentItem = self.currentItem + 1
#            self.docList[self.prevItem - 1].setBackground(QColor(35, 38, 41))
#            self.docList[self.currentItem - 1].setBackground(QColor(97, 138, 204))

#    def previousItem(self):
#        if len(self.docList) != 0:
#            if self.currentItem == 1:
#                self.prevItem = 1
#                self.currentItem = self.docLength
#            else:
#                self.prevItem = self.currentItem
#                self.currentItem = self.currentItem - 1
#            self.docList[self.prevItem - 1].setBackground(QColor(35, 38, 41))
#            self.docList[self.currentItem - 1].setBackground(QColor(97, 138, 204))

    def Open(self):
        self.resourceBrowser.Open(self.webAddress)
        
    def scrollDown(self):
        self.resourceBrowser.scrollDown()

    def scrollUp(self):
        self.resourceBrowser.scrollUp()

    def Close(self):
        self.resourceBrowser.Terminate()
