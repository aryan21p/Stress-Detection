import time


class BlinkRate:

    def __init__(self):

        self.start_time = time.time()
        self.blink_per_minute = 0

    def update(self, blink_count):

        elapsed = time.time() - self.start_time

        if elapsed >= 60:

            self.blink_per_minute = blink_count

            self.start_time = time.time()

            return self.blink_per_minute

        return self.blink_per_minute