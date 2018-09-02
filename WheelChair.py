from socket import *


class WheelChair:
    def __init__(self):
        host = "192.168.43.5"  # set to IP address of target computer
        port = 13000
        self.addr = (host, port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.active = False
        self.forward = False
        self.fan = False
        self.light = False

    def start(self):
        if self.active:
            print("WheelChair : start")
            self.socket.sendto(bytes('start'.encode()), self.addr)
            self.forward = True
        else:
            print("WheelChair is not active")

    def stop(self):
        if self.active:
            print("WheelChair : stop")
            self.socket.sendto(bytes('stop'.encode()), self.addr)
            self.forward = False
        else:
            print("WheelChair is not active")

    def toggleStartStop(self):
        if self.active:
            if self.forward:
                print("WheelChair : stop")
                self.socket.sendto(bytes('stop'.encode()), self.addr)
                self.forward = False
            else:
                print("WheelChair : start")
                self.socket.sendto(bytes('start'.encode()), self.addr)
                self.forward = True
        else:
            print("WheelChair is not active")

    def left(self):
        if self.active:
            print("WheelChair : left")
            self.socket.sendto(bytes('left'.encode()), self.addr)
        else:
            print("WheelChair is not active")

    def right(self):
        if self.active:
            print("WheelChair : right")
            self.socket.sendto(bytes('right'.encode()), self.addr)
        else:
            print("WheelChair is not active")

    def toggleFan(self):
        if self.fan:
            print("WheelChair : fan Off")
            self.socket.sendto(bytes('fanOff'.encode()), self.addr)
        else:
            print("WheelChair : fan On")
            self.socket.sendto(bytes('fanOn'.encode()), self.addr)

    def toggleLight(self):
        if self.fan:
            print("WheelChair : light Off")
            self.socket.sendto(bytes('lightOff'.encode()), self.addr)
        else:
            print("WheelChair : light On")
            self.socket.sendto(bytes('lightOn'.encode()), self.addr)

    def emergencyStop(self):
        self.forward = False
        self.socket.sendto(bytes('stop'.encode()), self.addr)
