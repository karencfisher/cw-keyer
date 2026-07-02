from gpiozero import TonalBuzzer, LED, DigitalOutputDevice
from time import sleep

from keyer.morse import MORSE_CODE


class Sender:
    def __init__(self, speed: int):
        self.speed = speed
        self.time_unit = 60 / (50 * speed)
        self.reverse_morse = {value: key for key, value in MORSE_CODE.items()}
        
        self.tone = TonalBuzzer(18)
        self.led = LED(13)
        self.tx_key = DigitalOutputDevice(6, initial_value=False)
        
    def send(self, message: str) -> None:
        message = message.upper()
        
        for i, char in enumerate(message):
            if char == ' ':
                self._key_up(4 * self.time_unit)
            else:
                code = self.reverse_morse.get(char)
                if code is None:
                    print('Unknown character: "{char}"')
                    continue
                
                for element in code:
                    timing = 3 * self.time_unit if element == '-' else self.time_unit
                    self._key_down(timing)
                    self._key_up(self.time_unit)

                self._key_up(2 * self.time_unit)
                
                    
    def _key_down(self, timing: float) -> None:
        self.tone.play(550)
        self.led.on()
        self.tx_key.on()
        sleep(timing)
        
    def _key_up(self, timing):
        self.tone.stop()
        self.led.off()
        self.tx_key.off()
        sleep(timing)
                    

    