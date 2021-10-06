#왠지 모르겠지만 sleep(0.0001)이렇게 낮은 타임으로 빠르게 동작시킨 후,
#해당 코드를 작동시키면 부드럽게 동작한다
# Stepper1.py
# 제대로 작동하는 코드, 속도는 delay로 조절가능하다
# 주의 : delay는 0.001일 때, 모터의 동작에 오류없이 작동하였다

import RPi.GPIO as GPIO
import time

P_A1 = 5  # adapt to your wiring
P_A2 = 6 # ditto
P_B1 = 12 # ditto
P_B2 = 13 # ditto
step = 16
delay = 0.001 # time to settle

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_A1, GPIO.OUT)
    GPIO.setup(P_A2, GPIO.OUT)
    GPIO.setup(P_B1, GPIO.OUT)
    GPIO.setup(P_B2, GPIO.OUT)

def forwardStep():
    setStepper(1, 0, 1, 0)
    setStepper(0, 1, 1, 0)
    setStepper(0, 1, 0, 1)
    setStepper(1, 0, 0, 1)

def backwardStep():
    setStepper(1, 0, 0, 1)
    setStepper(0, 1, 0, 1)
    setStepper(0, 1, 1, 0)
    setStepper(1, 0, 1, 0)
  
def setStepper(in1, in2, in3, in4):
    GPIO.output(P_A1, in1)
    GPIO.output(P_A2, in2)
    GPIO.output(P_B1, in3)
    GPIO.output(P_B2, in4)
    time.sleep(delay)

#GPIO.cleanup()
setup()
# 16 steps for 90 degrees, adapt to your motor
try:
    while True:
        print ("forward")
        for i in range(step):
            forwardStep() 
        time.sleep(2)
        print ("backward")
        for i in range(step):
            backwardStep() 
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
