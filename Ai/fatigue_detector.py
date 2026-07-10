class FatigueDetector:

    def __init__(self):

        self.score = 0
        self.level = "Low"

    def update(
        self,
        blink_rate,
        yawn_count,
        attention,
        stress,
        emotion
    ):

        score = 0

        # Blink Rate
        if blink_rate > 25:
            score += 25
        elif blink_rate > 15:
            score += 15

        # Yawning
        if yawn_count >= 3:
            score += 20
        elif yawn_count >= 1:
            score += 10

        # Attention
        if attention < 60:
            score += 25
        elif attention < 80:
            score += 10

        # Stress
        if stress == "High":
            score += 20
        elif stress == "Medium":
            score += 10

        # Emotion
        if emotion == "Sleepy":
            score += 20

        self.score = min(score, 100)

        if self.score < 30:
            self.level = "Low"

        elif self.score < 60:
            self.level = "Medium"

        else:
            self.level = "High"

        return self.score, self.level