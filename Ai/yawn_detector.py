import math
import time


class YawnDetector:

    def __init__(self):

        # Tune according to your camera
        self.MAR_THRESHOLD = 1.15

        # Mouth must stay open for these many frames
        self.MIN_OPEN_FRAMES = 15

        self.open_frames = 0
        self.yawning = False
        self.yawn_count = 0

        # Prevent duplicate counting
        self.last_yawn_time = 0
        self.COOLDOWN = 2.5  # seconds

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def update(self, landmarks):

        # No face
        if landmarks is None:
            return self.yawn_count, 0.0

        upper = landmarks[13]
        lower = landmarks[14]

        left = landmarks[78]
        right = landmarks[308]

        vertical = self.distance(upper, lower)
        horizontal = self.distance(left, right)

        if horizontal == 0:
            return self.yawn_count, 0.0

        mar = vertical / horizontal

        # Mouth Open
        if mar > self.MAR_THRESHOLD:

            self.open_frames += 1

            if self.open_frames >= self.MIN_OPEN_FRAMES:
                self.yawning = True

        # Mouth Closed
        else:

            if self.yawning:

                now = time.time()

                if (now - self.last_yawn_time) > self.COOLDOWN:
                    self.yawn_count += 1
                    self.last_yawn_time = now

            self.open_frames = 0
            self.yawning = False

        return self.yawn_count, mar