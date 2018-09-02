from socket import *


class WheelChair:
    def __init__(self):
        host = "192.168.43.5" # set to IP address of target computer
        port = 13000
        self.addr = (host, port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.is_going = False

    def start(self):
        # self.is_going = True
        print("start")
        if self.is_going:
            self.socket.sendto(bytes('start'.encode()), self.addr)

    def stop(self):
        print("stop")
        # self.is_going = False
        if self.is_going:
            self.socket.sendto(bytes('stop'.encode()), self.addr)

    def toggleStartStop(self):
        if self.is_going is True:
            print("disable")
            self.socket.sendto(bytes('stop'.encode()), self.addr)
            self.is_going = False
        else:
            print("enable")
            self.socket.sendto(bytes('start'.encode()), self.addr)
            self.is_going = True

    def left(self):
        print("left")
        if self.is_going:
            self.socket.sendto(bytes('left'.encode()), self.addr)

    def right(self):
        print("right")
        if self.is_going:
            self.socket.sendto(bytes('right'.encode()), self.addr)

    def playFan(self):
        self.socket.sendto(bytes('fan'.encode()), self.addr)

    def playLight(self):
        self.socket.sendto(bytes('light'.encode()), self.addr)
