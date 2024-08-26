import math
import time
import globals

class GameTimer:
    def __init__(self):
        pass

    start_time = 0
    elapsed_time = 0
    stopped: bool = False
    started: bool = False
    _minutes: int = 0
    _seconds: int = 0

    def draw(self):
        if not globals.game_paused and not self.stopped and self.started:
            self.elapsed_time = math.ceil(time.time() - self.start_time)
            self._minutes = self.elapsed_time // 60
            self._seconds = self.elapsed_time % 60

    def start(self):
        self.started = True
        self.stopped = False
        self.start_time = time.time()

    def display_minutes(self):
        if self._minutes == 0:
            return "00"
        elif self._minutes < 10:
            return f"0{str(self._minutes)}"
        else:
            return str(self._minutes)
        
    def display_seconds(self):
        if self._seconds == 0:
            return "00"
        elif self._seconds < 10:
            return f"0{str(self._seconds)}"
        else:
            return str(self._seconds)
        
    def display(self):
        return f"{self.display_minutes()}:{self.display_seconds()}"