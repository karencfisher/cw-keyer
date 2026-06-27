from threading import Queue

from decoder.timing_model import TimingModel


ELEMENT_THRESHOLD_SCALAR = 2.0
WORD_GAP_THRESHOLD_SCALAR = 5.0

class Decoder:
    def __init__(self, decoder_queue: Queue, timing: TimingModel):
        self.decoder_queue = decoder_queue
        self.timing = timing
        
    def decode_stream(self):
        pass
        
    

