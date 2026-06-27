from threading import Thread, Queue

from keyer import Keyer
from decoder.timing_model import TimingModel
from decoder.decode import Decoder


def main():
    decoder_queue = Queue()
    timing = TimingModel()
    keyer = Keyer(timing, decoder_queue)

    gpio_daemon = Thread(function=keyer.run, daemon=True)
    gpio_daemon.start()

    decoder = Decoder(decoder_queue, timing).decode_stream()

    for text in decoder:
        print(text, end="", flush=True)
        
        
if __name__ == '__main__':
    main()
        