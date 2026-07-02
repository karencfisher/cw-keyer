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
        
    def run(self):
        event_queue = EventQueue(self.timing, self.decoder_queue, debug=self.debug)

        tone = TonalBuzzer(18)
        led = LED(13)

        key = Button(26, pull_up=True, bounce_time=0.05)
        tx_key = DigitalOutputDevice(6, initial_value=False)

        def key_down():
            led.on()
            tx_key.on()
            tone.play(550)   # 550 Hz
            
            event_queue.enqueue_event('DOWN')

        def key_up():
            tone.stop()
            led.off()
            tx_key.off()
            
            event_queue.enqueue_event('UP')

        key.when_activated = key_down
        key.when_deactivated = key_up

        pause()
