import pyglet
import os


class ResourceMusic:

    def __init__(self):
        self.player = pyglet.media.Player()
        pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

    def playMusic(self, musicName):
        self.stopMusic()
        self.path = os.path.join("C:\\Users\\prant\\Desktop\\Final\\EyeTask\\MusicFiles", musicName)
        self.source = pyglet.media.load(self.path, streaming=False)
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
