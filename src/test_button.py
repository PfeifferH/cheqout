import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

red = 23
yellow = 24
green = 25

GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pre_input = None

while True:
    if (GPIO.input(red) and pre_input != 'red'):
        print("red")
        pre_input = 'red'
    elif (GPIO.input(yellow) and pre_input != 'yellow'):
        print("yellow")
        pre_input = 'yellow'
    elif (GPIO.input(green) and pre_input != 'green'):
        print("green")
        pre_input = 'green'
