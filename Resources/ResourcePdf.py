import subprocess
import pyautogui


class ResourcePdf:

    def Open(self, docName):
        file = "C:\\Users\\prant\\Desktop\\Final\\EyeTask\\Documents\\" + docName
        self.process = subprocess.Popen(["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", file])

    def scrollDown(self):
        pyautogui.press('down')

    def scrollUp(self):
        pyautogui.press('up')

    def Terminate(self):
        self.process.terminate()
