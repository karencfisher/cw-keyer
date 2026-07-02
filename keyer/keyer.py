from gpiozero import TonalBuzzer, LED, Button, DigitalOutputDevice
from signal import pause
from queue import Queue

from keyer.decoder.events import EventQueue
from keyer.decoder.timing_model import TimingModel


class Keyer:
    def __init__(self, timing: TimingModel, decoder_queue: Queue, debug: bool=False):
        self.timing = timing
        self.decoder_queue = decoder_queue
        self.debug = debug
        
        self.event_queue = EventQueue(self.timing, self.decoder_queue, debug=self.debug)
        self.tone = TonalBuzzer(18)
        self.led = LED(13)
        self.key = Button(26, pull_up=True, bounce_time=0.05)
        self.tx_key = DigitalOutputDevice(6, initial_value=False)
        
    def run(self):
        

        def key_down():
            self.led.on()
            self.tx_key.on()
            self.tone.play(550)   # 550 Hz
            
            self.event_queue.enqueue_event('DOWN')

        def key_up():
            self.tone.stop()
            self.led.off()
            self.tx_key.off()
            
            self.event_queue.enqueue_event('UP')

        self.key.when_activated = key_down
        self.key.when_deactivated = key_up

        pause()
