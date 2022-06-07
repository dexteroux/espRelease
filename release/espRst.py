#!/usr/bin/python3

import argparse
import RPi.GPIO as GPIO
import time

#rpi_pow = 17
esp_en = 17
esp_boot = 27

parser = argparse.ArgumentParser(description='Enable Boot mode for programming ESP.')
parser.add_argument('duration', metavar='N', type=int, nargs='?', default=1,
                    help='duration in seconds')

args = parser.parse_args()
duration = args.duration

GPIO.setmode(GPIO.BCM)

#GPIO.setup(rpi_pow, GPIO.OUT) 
#GPIO.setup(esp_en,   GPIO.OUT) 
GPIO.setup(esp_boot, GPIO.OUT) 

for i in range(duration):
    GPIO.output(esp_boot, 0)
    print(duration - i, "seconds to elapsed ...")
    time.sleep(1)


GPIO.setup(esp_boot, GPIO.IN) 
#GPIO.setup(esp_en, GPIO.OUT) 
#GPIO.output(esp_en, 0)
#time.sleep(3)

GPIO.cleanup()
