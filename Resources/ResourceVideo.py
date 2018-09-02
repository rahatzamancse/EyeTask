import subprocess
import pyautogui


class ResourceVideo:
    
    def __init__(self):
        self.process = None
    
    def playVideo(self,VideoName):
       file = "F:\\1Study\\projects\\EyeTask-V1.0\\VideoFiles\\" + VideoName
       self.process = subprocess.Popen(["E:\\1installed\\KMPlayer\\KMPlayer.exe", file])
    
    def pause(self):
        pyautogui.press('space')
        
    def resume(self):
        pyautogui.press('space')
        
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None