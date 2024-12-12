import time


class RunTimer:
    start: float

    def __init__(self):
        self.start = time.time()

    def get_time(self) -> float:
        return time.time() - self.start

    def print(self):
        print(f"Runtime: {self.get_time()}")