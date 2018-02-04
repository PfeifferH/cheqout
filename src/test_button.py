import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

red = 23
yellow = 24
green = 25

GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if (GPIO.input(red)):
        print("red")
    elif (GPIO.input(yellow)):
        print("yellow")
    elif (GPIO.input(green)):
        print("green")
