class AttentionDetector:

    def __init__(self):
        self.score = 100
        self.status = "Focused"

    def update(self, head, eyes):

        if not eyes:
            self.score = 20

        elif head == "Center":
            self.score = 100

        elif head == "Left":
            self.score = 40

        elif head == "Right":
            self.score = 40

        else:
            self.score = 70

        if self.score >= 80:
            self.status = "Focused"

        elif self.score >= 50:
            self.status = "Distracted"

        else:
            self.status = "Not Focused"

        return self.score, self.status