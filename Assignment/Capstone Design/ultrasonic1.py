import RPi.GPIO as GPIO
import time

print("HC-SR04 Start")

GPIO.setmode(GPIO.BCM)
# Pin 16 : 23(Trig)
GPIO.setup(23, GPIO.OUT)
# Pin 15 : 22(Echo)
GPIO.setup(22, GPIO.IN)

try:
    while True:
        GPIO.output(23, False)
        time.sleep(0.5)

        GPIO.output(23, True)
        time.sleep(0.00001)
        GPIO.output(23, False)

        while GPIO.input(22) == 0:
            start = time.time()

        while GPIO.input(22) == 1:
            stop = time.time()

        time_interval = stop - start
        distance = time_interval * 17000
        distance = round(distance, 2)

        print("Distance => ", distance, "cm")

except KeyboardInterrupt:
    GPIO.cleanup()
    print("HC-SR04 End")