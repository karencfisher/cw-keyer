from decoder.timing_model import TimingModel
from decoder.events import EventQueue


ELEMENT_THRESHOLD_SCALAR = 2.0
WORD_GAP_THRESHOLD_SCALAR = 5.0

class Decoder:
    def __init__(self, events: EventQueue, timing: TimingModel):
        self.events = events
        self.timing = timing
        
    

