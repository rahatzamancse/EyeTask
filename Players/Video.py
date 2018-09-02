import os,fnmatch

from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import(QStandardItemModel,QStandardItem,QColor,QFont)
from Resources.ResourceVideo import ResourceVideo

class Video:
    
    def __init__(self):
        self.mediaLength = 0
        self.mediaList = []
        self.formats = ['*.mp4','*.flv','*.mpeg','*.mkv']
        self.playing = False
        self.resuming = False
        self.initUI()

    def togglePlay(self):
        
        if len(self.mediaList) != 0:
            
            if not self.playing:
                self.play()
                self.playing = True
            elif self.resuming:
                self.pause()
                self.resuming = False
            else:
                self.resume()
                self.resuming = True

    def initUI(self):
	
        self.list = QListView()
        self.list.setWindowTitle("Video Files")
        self.list.setMinimumSize(300,400)
        self.list.setSpacing(10)
        self.model = QStandardItemModel(self.list)
        self.resourceVideo = ResourceVideo()
        
        for root,dirs,files in os.walk("VideoFiles"):
            for extensions in self.formats:
                for filename in fnmatch.filter(files,extensions):
                    item = QStandardItem(filename)
                    item.setFont(QFont(filename,10))
                    self.model.appendRow(item)
                    self.mediaList.append(item)
        
        self.mediaLength = len(self.mediaList)

        self.currentItem = 1
        
        self.prevItem = self.mediaLength
        
        if len(self.mediaList) != 0:
            self.mediaList[0].setBackground(QColor(97,138,204))
        
        self.list.setModel(self.model)
        
        self.list.show()
        
    def nextItem(self):
        
        if len(self.mediaList) != 0:
        
            if(self.currentItem == self.mediaLength):
                
                self.prevItem = self.mediaLength
                
                self.currentItem = 1
                
            else:
                
                self.prevItem = self.currentItem
                
                self.currentItem = self.currentItem + 1
                
            self.mediaList[self.prevItem - 1].setBackground(QColor(35,38,41))    
                
            self.mediaList[self.currentItem - 1].setBackground(QColor(97,138,204))
        
        
#    def previousItem(self):
#      if len(self.mediaList) != 0:  
#        if(self.currentItem == 1):
#            
#            self.prevItem = 1
#            
#            self.currentItem = self.mediaLength
#            
#        else:
#            
#            self.prevItem = self.currentItem
#            
#            self.currentItem = self.currentItem - 1
#            
#        self.mediaList[self.prevItem - 1].setBackground(QColor(35,38,41))    
#            
#        self.mediaList[self.currentItem - 1].setBackground(QColor(97,138,204))
        
    def play(self):
 
        self.resourceVideo.playVideo(self.mediaList[self.currentItem - 1].text())
        return 1
        
    def pause(self):
        
        self.resourceVideo.pause()
        
    def resume(self):
        self.resourceVideo.resume()
        
    def stop(self):
        
        if len(self.mediaList) != 0:
            
            self.resourceVideo.stop()
            self.playing = False
            self.resuming = False
    
    def Close(self):
        self.list.close()