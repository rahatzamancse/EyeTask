import subprocess
import pyautogui


class ResourceVideo:
    
    def __init__(self):
        self.process = None
    
    def playVideo(self,VideoName):
       file = "C:\\Users\\prant\\Desktop\\Final\\EyeTask\\VideoFiles\\" + VideoName
       self.process = subprocess.Popen(["C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe", file])
    
    def pause(self):
        pyautogui.press('space')
        
    def resume(self):
        pyautogui.press('space')
        
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
