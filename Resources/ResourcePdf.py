import subprocess
import pyautogui


class ResourcePdf:

    def Open(self, docName):
        file = "C:\\Users\\prant\\Desktop\\Final\\EyeTask\\Documents" + docName
        self.process = subprocess.Popen(["C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe", file])

    def scrollDown(self):
        pyautogui.press('down')

    def scrollUp(self):
        pyautogui.press('up')

    def Terminate(self):
        self.process.terminate()
