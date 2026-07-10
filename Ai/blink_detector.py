class BlinkDetector:

    def __init__(self, threshold=0.26):

        self.threshold = threshold

        self.eye_closed = False

        self.blink_count = 0

    def update(self, ear):

        # Eyes Closed
        if ear < self.threshold:

            self.eye_closed = True

        # Eyes Open Again
        else:

            if self.eye_closed:

                self.blink_count += 1

            self.eye_closed = False

        return self.blink_count