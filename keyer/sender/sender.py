from gpiozero import TonalBuzzer, LED, Button, DigitalOutputDevice

from keyer.morse import MORSE_CODE


class Sender:
    def __init__(self, speed: int):
        self.speed = speed
        self.time_unit = 60 / (50 * speed)
        self.reverse_morse = {value: key for key, value in MORSE_CODE.items()}
        
    def send(self, message: str):
        pass

    