class StressDetector:

    def __init__(self):
        self.stress = "Calm"

    def update(self, blink_count, ear):

        if blink_count >= 25:
            self.stress = "High"

        elif blink_count >= 15:
            self.stress = "Medium"

        else:
            self.stress = "Calm"

        return self.stress