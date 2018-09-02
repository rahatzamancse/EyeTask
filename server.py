#!/usr/bin/python
# -*- coding: utf-8 -*-
# import os

import RPi.GPIO as GPIO
from socket import *



left_speed = 21
right_speed = 22
leftMotor = {'+': 11, '-': 7}
rightMotor = {'+': 15, '-': 13}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.PWM(left_speed, 2000).start(21)
GPIO.PWM(right_speed, 2000).start(22)


def leftMotorGo(dir):
    print('left : ' + dir)
    if dir is 'front':
        GPIO.output(leftMotor['+'], True)
        GPIO.output(leftMotor['-'], False)
    else:
        GPIO.output(leftMotor['+'], False)
        GPIO.output(leftMotor['-'], False)


def rightMotorGo(dir):
    print('right : ' + dir)
    if dir is 'front':
        GPIO.output(rightMotor['+'], True)
        GPIO.output(rightMotor['-'], False)
    else:
        GPIO.output(rightMotor['+'], False)
        GPIO.output(rightMotor['-'], False)


def up():
    leftMotorGo('front')
    rightMotorGo('front')


def down():
    leftMotorGo('stop')
    rightMotorGo('stop')


def left():
    leftMotorGo('stop')
    rightMotorGo('front')


def right():
    leftMotorGo('front')
    rightMotorGo('stop')


def main():
    host = "192.168.1.4"
    port = 13000
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print('Waiting to receive messages...')

    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        data = data.decode('utf-8')
        print('Received message: ' + data)
        if data == 'start':
            up()
        elif data == 'stop':
            down()
        elif data == 'right':
            right()
        elif data == 'left':
            left()

    UDPSock.close()
    os._exit(0)

main()
