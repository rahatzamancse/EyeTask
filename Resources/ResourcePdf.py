import subprocess
import pyautogui


class ResourcePdf:

    def Open(self, docName):
        file = "F:\\1Study\\projects\\EyeTask-V2.0\\Documents" + docName
        self.process = subprocess.Popen(["C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe", file])

    def scrollDown(self):
        pyautogui.press('down')

    def scrollUp(self):
        pyautogui.press('up')

    def Terminate(self):
        self.process.terminate()
