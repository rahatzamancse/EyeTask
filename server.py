import RPi.GPIO as GPIO
from socket import *

leftMotor = {'+': 13, '-': 11}
rightMotor = {'+': 5, '-': 3}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

pwm1 = GPIO.PWM(7, 100)
pwm2 = GPIO.PWM(15, 100)
pwm1.start(0)
pwm2.start(0)
pwm1.changeDutyCycle(99)
pwm2.changeDutyCycle(99)

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

def setSpeed(val):
    print("DutyCycle : " + str(val))
    pwm1.changeDutyCycle(val)
    pwm2.changeDutyCycle(val)

def main():
    host = "192.168.0.15"
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
        elif data[0:3] == "set":
            setSpeed(int(data[3:]))

    UDPSock.close()
    os._exit(0)

main()
