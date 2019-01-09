import os


def set_boiler_high():
    return


def set_boiler_low():
    return

if not os.getenv("LOCAL"):
    import RPi.GPIO as GPIO

    RELAY_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)


    def set_boiler_high():
        GPIO.output(RELAY_PIN, GPIO.HIGH)


    def set_boiler_low():
        GPIO.output(RELAY_PIN, GPIO.LOW)
