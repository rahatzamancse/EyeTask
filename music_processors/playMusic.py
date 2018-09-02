import pyglet
import os

class ResourceMusic:

    
    def __init__(self):
        
        pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

        self.script_dir = os.path.dirname(__file__)
    
    def playMusic(self,musicName):
        
            self.stopMusic()
            
            self.player = pyglet.media.Player()
        
            self.path = os.path.join(self.script_dir, musicName)
                    
            self.source = pyglet.media.load(self.path,streaming=False)
                    
            self.player.queue(self.source)
            
            self.player.play()
        
    
    def pauseMusic(self):
        
        try:
            
            self.player.pause()
        
        except:
            
            return
    
    def stopMusic(self):
        
        try:
            
           self.pauseMusic()
    
           del self.source
        
           del self.player
            
        except:
            
            return
            
    def resumeMusic(self):
        
        try:
            
            self.player.play()
            
        except:
            
            return
