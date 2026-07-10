class EmotionDetector:

    def __init__(self):
        self.emotion = "Neutral"

    def update(self, ear, mar):

        # Sleepy
        if ear < 0.22:
            self.emotion = "Sleepy"

        # Mouth open
        elif mar > 0.85:
            self.emotion = "Surprised"

        # Normal
        else:
            self.emotion = "Neutral"

        return self.emotion