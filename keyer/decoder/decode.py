from queue import Queue, Empty

from keyer.decoder.timing_model import TimingModel
from keyer.morse import MORSE_CODE


ELEMENT_THRESHOLD_SCALAR = 2.0
WORD_GAP_THRESHOLD_SCALAR = 5.0
EOM_SCALAR = 7.5

class Decoder:
    def __init__(self, decoder_queue: Queue, timing: TimingModel):
        self.decoder_queue = decoder_queue
        self.timing = timing
        
    def decode_stream(self):
        event_buffer = []
        sending = False
        while True:
            if not self.timing.ready:
                continue
            
            try:
                event = self.decoder_queue.get(timeout=EOM_SCALAR * self.timing.dit_ms / 1000)
            except Empty:
                token = "<EOM>"
            else:
                token = self._classify_event(event, self.timing)

            if token in (".", "-"):
                event_buffer.append(token)
                sending = True
            elif token == "<EOM>":
                if event_buffer:
                    yield self._get_char(event_buffer) + " "
                elif sending:
                    sending = False
                    yield "\n\n"
            elif token in ("<EOC>", "<EOW>") and event_buffer:
                yield self._get_char(event_buffer) + (" " if token == "<EOW>" else "")
                    
    def _get_char(self, event_buffer: list[str]) -> str:
        code = "".join(event_buffer)
        event_buffer.clear()
        return MORSE_CODE.get(code, "*")
                    
    def _classify_event(self, event, timing) -> str:
        if event.state == "DOWN":
            return "-" if event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms else "."

        if event.duration_ms > WORD_GAP_THRESHOLD_SCALAR * timing.dit_ms:
            return "<EOW>"
        elif event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms:
            return "<EOC>"
        else:
            return ""
        
    

