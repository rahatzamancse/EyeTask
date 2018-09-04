import subprocess
import pyautogui


class ResourceBrowser:
    def Open(self, address):
        self.process = subprocess.Popen(["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", address])

    def scrollDown(self):
        pyautogui.press('down')

    def scrollUp(self):
        pyautogui.press('up')

    def Terminate(self):
        self.process.terminate()
