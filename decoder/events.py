from dataclasses import dataclass
from collections import deque
from time import perf_counter_ns

from decoder.timing_model import TimingModel


@dataclass
class Event:
    state: str          # "DOWN" or "UP"
    timestamp_ns: int
    duration_ms: int = 0
    
    
class EventQueue:
    def __init__(self, timing: TimingModel, debug: bool=False):
        self.event_queue = deque()
        self.timing = timing
        self.down_times = []
        self.debug = debug
        
    def __len__(self) -> int:
        return len(self.event_queue)
        
    def enqueue_event(self, state: str) -> None:
        self.event_queue.append(Event(state, perf_counter_ns()))
        elapsed = 0
        if len(self.event_queue) > 1:
            current, previous = self.peek_event(-1), self.peek_event(-2)
            elapsed = current.timestamp_ns - previous.timestamp_ns
            elapsed //= 1_000_000
            previous.duration_ms = elapsed
            
            if previous.state == 'DOWN' and elapsed > 0:
                  self.down_times.append(elapsed)
                  
        # Bootstrap timings
        if len(self.down_times) > 1 and not self.timing.ready:
            if self.timing.try_bootstrap(self.down_times):
                self.down_times.clear()
                if self.debug:
                    print(f"Timing found: dit={self.timing.dit_ms:.1f} ms,",
                        f"dah={self.timing.dah_ms:.1f} ms")
                        
        # Update timings
        if len(self.down_times) >= 10 and self.timing.ready:
            if self.timing.refine_centers(self.down_times):
                self.down_times.clear()
                if self.debug:
                    print(f"Timing found: dit={self.timing.dit_ms:.1f} ms,",
                        f"dah={self.timing.dah_ms:.1f} ms")
        
    def peek_event(self, index: int=0) -> Event:
        if index >= len(self.event_queue):
            return None
        return self.event_queue[index]
    
    def dequeue_event(self) -> Event:
        return self.event_queue.popleft()
    