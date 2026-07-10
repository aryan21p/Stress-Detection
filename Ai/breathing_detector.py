import cv2
import time
import numpy as np


class BreathingDetector:

    def __init__(self):

        self.prev_gray = None
        self.motion_history = []

        self.start_time = time.time()
        self.last_peak_time = time.time()

        self.breath_count = 0
        self.rate = 0

    def update(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        h, w = gray.shape

        # Chest Region (ROI)
        roi = gray[
            int(h * 0.45):int(h * 0.80),
            int(w * 0.30):int(w * 0.70)
        ]

        if self.prev_gray is None:
            self.prev_gray = roi
            return self.rate

        diff = cv2.absdiff(self.prev_gray, roi)

        motion = np.mean(diff)

        self.motion_history.append(motion)

        self.prev_gray = roi

        if len(self.motion_history) > 60:
            self.motion_history.pop(0)

        # Peak Detection
        if len(self.motion_history) >= 3:

            a = self.motion_history[-3]
            b = self.motion_history[-2]
            c = self.motion_history[-1]

            if b > a and b > c and b > 2.5:

                now = time.time()

                if now - self.last_peak_time > 2:

                    self.breath_count += 1
                    self.last_peak_time = now

        elapsed = time.time() - self.start_time

        if elapsed > 0:
            self.rate = int(self.breath_count * 60 / elapsed)

        return self.rate