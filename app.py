from threading import Thread
from queue import Queue
from signal import pause

from keyer.keyer import Keyer
from keyer.decoder.timing_model import TimingModel
from keyer.decoder.decode import Decoder


def main():
    decoder_queue = Queue()
    timing = TimingModel()
    keyer = Keyer(timing, decoder_queue, debug=False)

    gpio_daemon = Thread(target=keyer.run, daemon=True)
    gpio_daemon.start()
    
    print('Started...')

    decoder = Decoder(decoder_queue, timing).decode_stream()

    for text in decoder:
        print(text, end="", flush=True)
    # pause()   
        
if __name__ == '__main__':
    main()
        