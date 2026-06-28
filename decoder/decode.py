from queue import Queue

from decoder.timing_model import TimingModel
from decoder.morse import MORSE_CODE


ELEMENT_THRESHOLD_SCALAR = 2.0
WORD_GAP_THRESHOLD_SCALAR = 5.0

class Decoder:
    def __init__(self, decoder_queue: Queue, timing: TimingModel):
        self.decoder_queue = decoder_queue
        self.timing = timing
        
    def decode_stream(self):
        event_buffer = []
        while True:
            if not self.timing.ready:
                continue
            
            event = self.decoder_queue.get()
            token = self._classify_event(event, self.timing)

            if token in (".", "-"):
                event_buffer.append(token)
            elif token in ("<EOC>", "<EOW>"):
                if event_buffer:
                    code = "".join(event_buffer)
                    char = MORSE_CODE.get(code, "*")
                    event_buffer.clear()
                    yield char + (" " if token == "<EOW>" else "")
                    
    def _classify_event(self, event, timing):
        if event.state == "DOWN":
            return "-" if event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms else "."

        if event.duration_ms > WORD_GAP_THRESHOLD_SCALAR * timing.dit_ms:
            return "<EOW>"
        elif event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms:
            return "<EOC>"
        else:
            return ""
        
    

