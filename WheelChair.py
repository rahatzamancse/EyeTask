from socket import *


class WheelChair:
    def __init__(self):
        host = "192.168.0.14"  # set to IP address of target computer
        port = 13000
        self.addr = (host, port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.fan = False
        self.light = False
        self.state = "stop"

    def start(self):
        if self.state != "start":
            print("WheelChair : start")
            self.socket.sendto(bytes('start'.encode()), self.addr)
            self.state = "start"

    def stop(self):
        if self.state != "stop":
            print("WheelChair : stop")
            self.socket.sendto(bytes('stop'.encode()), self.addr)
            self.state = "stop"

    def toggleStartStop(self):
        if self.state != "stop":
            print("WheelChair : stop")
            self.socket.sendto(bytes('stop'.encode()), self.addr)
            self.state = "stop"
        else:
            print("WheelChair : start")
            self.socket.sendto(bytes('start'.encode()), self.addr)
            self.state = "start"

    def left(self):
        if self.state != "left":
            print("WheelChair : left")
            self.socket.sendto(bytes('left'.encode()), self.addr)
            self.state = "left"

    def right(self):
        if self.state != "right":
            print("WheelChair : right")
            self.socket.sendto(bytes('right'.encode()), self.addr)
            self.state = "right"

    def toggleFan(self):
        if self.fan:
            print("WheelChair : fan Off")
            self.socket.sendto(bytes('fanOff'.encode()), self.addr)
        else:
            print("WheelChair : fan On")
            self.socket.sendto(bytes('fanOn'.encode()), self.addr)

    def toggleLight(self):
        if self.light:
            print("WheelChair : light Off")
            self.socket.sendto(bytes('lightOff'.encode()), self.addr)
        else:
            print("WheelChair : light On")
            self.socket.sendto(bytes('lightOn'.encode()), self.addr)

    def emergencyStop(self):
        self.stop()

    def setSpeed(self, val):
        self.socket.sendto(bytes(('set ' + str(val)).encode()), self.addr)
