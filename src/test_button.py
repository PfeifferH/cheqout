import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

red = 23
yellow = 24
green = 25

GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pre_red = False
pre_yellow = False
pre_green = False

while True:
    if GPIO.input(red) and not pre_red:
        print("red")
        pre_red = True
    else:
        pre_red = False
    if GPIO.input(yellow) and not pre_yellow:
        print("yellow")
        pre_yellow = True
    else:
        pre_yellow = False
    if GPIO.input(green) and not pre_green:
        print("green")
        pre_green = True
    else:
        pre_green = False
