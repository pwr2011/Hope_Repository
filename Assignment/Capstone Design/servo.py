# duty cycle available : 2~13
# 7로 두기.
import RPi.GPIO as GPIO
import time
import keyboard
import numpy

def to_left():
    i = 7
    while i>=4.5:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i-0.125
    while i<=7:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125

def to_right():
    i = 7
    while i<=9.5:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125
    while i>=7:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time )
        i = i-0.125


pin = 12 # PWM pin num 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
p.ChangeDutyCycle(7)
time.sleep(2)
sleep_time = 0.2

try:
    while True:
        a = int(input())
        if a == 1:
            to_left()
        else:
            to_right()

except KeyboardInterrupt:
    p.stop()

GPIO.cleanup()
