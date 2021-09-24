import RPi.GPIO as GPIO
import time

print("HC-SR04 Start")

GPIO.setmode(GPIO.BCM)
# Pin 13 : 27(Trig)
GPIO.setup(27, GPIO.OUT)
# Pin 11 : 17(Echo)
GPIO.setup(17, GPIO.IN)

try:
    while True:
        GPIO.output(27, False)
        time.sleep(0.5)

        GPIO.output(27, True)
        time.sleep(0.00001)
        GPIO.output(27, False)

        while GPIO.input(17) == 0:
            start = time.time()

        while GPIO.input(17) == 1:
            stop = time.time()

        time_interval = stop - start
        distance = time_interval * 17000
        distance = round(distance, 2)

        print("Distance => ", distance, "cm")

except KeyboardInterrupt:
    GPIO.cleanup()
    print("HC-SR04 End")