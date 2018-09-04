from Resources.ResourceBrowser import ResourceBrowser


class Browser:
    def __init__(self, address):
        self.webAddress = address
        self.resourceBrowser = ResourceBrowser()
        self.Open()

    def Open(self):
        self.resourceBrowser.Open(self.webAddress)

    def scrollDown(self):
        self.resourceBrowser.scrollDown()

    def scrollUp(self):
        self.resourceBrowser.scrollUp()

    def Close(self):
        self.resourceBrowser.Terminate()
