#import modules
import Rpi.Gpio as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

def switchoff():
    print ("Switch Off")
    GPIO.output(18,GPIO.LOW)

def switchon():
    print ("Switch Off")
    GPIO.output(18,GPIO.HIGH)

def blink():
    switchoff();
    time.sleep(5);
    switchon()

blink()