import fnmatch
import os

from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QColor, QFont)
from PyQt5.QtWidgets import QListView

from Resources.ResourcePdf import ResourcePdf


class Document:
    def __init__(self):
        self.currentItem = 1
        self.resourcePdf = ResourcePdf()
        self.list = QListView()
        self.model = QStandardItemModel(self.list)
        self.isOpen = 0
        self.docLength = 0
        self.docList = []
        self.formats = ['*.pdf']
        self.prevItem = self.docLength
        self.initUI()

    def destroy(self):
        self.list.close()
        return -1

    def initUI(self):
        self.list.setWindowTitle("Documents")
        self.list.setMinimumSize(300, 400)
        self.list.setSpacing(10)

        for root, dirs, files in os.walk("Documents"):
            for extensions in self.formats:
                for filename in fnmatch.filter(files, extensions):
                    item = QStandardItem(filename)
                    item.setFont(QFont(filename, 10))
                    self.model.appendRow(item)
                    self.docList.append(item)

        self.docLength = len(self.docList)
        if len(self.docList) != 0:
            self.docList[0].setBackground(QColor(97, 138, 204))
        self.list.setModel(self.model)
        self.list.show()

    def nextItem(self):
        if len(self.docList) != 0:
            if self.currentItem == self.docLength:
                self.prevItem = self.docLength
                self.currentItem = 1
            else:
                self.prevItem = self.currentItem
                self.currentItem = self.currentItem + 1
            self.docList[self.prevItem - 1].setBackground(QColor(35, 38, 41))
            self.docList[self.currentItem - 1].setBackground(QColor(97, 138, 204))

    def Open(self):
        if len(self.docList) != 0:
            self.resourcePdf.Open(self.docList[self.currentItem - 1].text())
            return True
        else:
            return False
        
    def scrollDown(self):
        self.resourcePdf.scrollDown()

    def scrollUp(self):
        self.resourcePdf.scrollUp()

    def Close(self):
        self.resourcePdf.Terminate()
