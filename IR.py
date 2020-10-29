import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

while True:
 sensor = GPIO.input(26)
 print(sensor)
 if sensor == 1:
  print("NO")
  sleep(0.1)
 elif sensor == 0:
  print("YES")