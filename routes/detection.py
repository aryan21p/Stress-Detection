from Ai.recommendation import Recommendation
from Ai.fatigue_detector import FatigueDetector
from Ai.emotion_detector import EmotionDetector
from Ai.yawn_detector import YawnDetector
from Ai.breathing_detector import BreathingDetector
from Ai.attention_detector import AttentionDetector
from Ai.head_pose import detect_head_pose
from Ai.blink_rate import BlinkRate
from Ai.stress_detector import StressDetector
from Ai.blink_detector import BlinkDetector
from flask import Blueprint, render_template, Response, jsonify
import cv2

from Ai.face_detector import detect_face
from Ai.eye_tracking import detect_eyes


detection = Blueprint("detection", __name__)

camera = cv2.VideoCapture(0)


#this is Object
blink_detector = BlinkDetector()
stress_detector = StressDetector()
blink_rate = BlinkRate()
attention_detector = AttentionDetector()
breathing_detector = BreathingDetector()
yawn_detector = YawnDetector()
emotion_detector = EmotionDetector()
fatigue_detector = FatigueDetector()
recommendation = Recommendation()


# Global Variables
face_detected = False
eye_detected = False
head_direction = "Center"
attention_score = 100
attention_status = "Focused"
breathing_rate = 0
yawn_count = 0
emotion = "Neutral"

fatigue_score = 0
fatigue_level = "Low"

health_recommendation = "You are healthy"



EAR_THRESHOLD = 0.23


def generate_frames():

    global face_detected
    global eye_detected
    global head_direction

    global attention_score
    global attention_status
    global breathing_rate
    global yawn_count
    global emotion

    global fatigue_score
    global fatigue_level
    
    global health_recommendation
    
    
    
   

    while True:

        success, frame = camera.read()

        if not success:
            break

        if frame is None:
            continue

        # ---------------- FACE DETECTION ----------------
        frame, detected = detect_face(frame)

        # ---------------- EYE DETECTION -----------------
        frame, eyes, ear, landmarks = detect_eyes(frame)

        #head pose
        frame, head_direction = detect_head_pose(frame)

        face_detected = detected
        eye_detected = eyes

        # # ---------------- BLINK DETECTION ---------------
        if detected:
         blink_count = blink_detector.update(ear)
         blink_per_min = blink_rate.update(blink_count)
         stress = stress_detector.update(blink_count, ear)

         attention_score, attention_status = attention_detector.update(
         head_direction,
          eye_detected
         )
         breathing_rate = breathing_detector.update(frame)
         mar=0
         if landmarks is not None:
          yawn_count, mar = yawn_detector.update(landmarks)
          print(f"MAR = {mar:.3f}")
         cv2.putText(
           frame,
           f"MAR:{mar:.2f}",
           (20, 80),
           cv2.FONT_HERSHEY_SIMPLEX,
           1,
           (0, 255, 255),
           2
         )
         emotion = emotion_detector.update(
          ear,
          mar
         )

         fatigue_score, fatigue_level = fatigue_detector.update(
           blink_per_min,
           yawn_count,
           attention_score,
           stress_detector.stress,
           emotion
         )

         health_recommendation = recommendation.get(
          fatigue_score,
          stress_detector.stress,
          attention_score,
          emotion
         )


         
        # if detected:

        #     if ear < EAR_THRESHOLD:

        #         closed_frames += 1

        #         if closed_frames >= 2:
        #             blink_started = True

        #     else:

        #         if blink_started:
        #             blink_count += 1

        #         blink_started = False
        #         closed_frames = 0

        #         print(f"EAR = {ear:.3f}")

        # Uncomment only for debugging
        # print(f"EAR: {ear:.2f} | Blink: {blink_count}")

        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


@detection.route("/detection")
def detection_page():
    return render_template("detection.html")


@detection.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@detection.route("/status")
def status():

    return jsonify({
        "face": "Detected" if face_detected else "Not Detected",
        "eyes": "Open" if eye_detected else "Closed",
        "blink": blink_detector.blink_count,
        "blink_per_min": blink_rate.blink_per_minute,
        "stress": stress_detector.stress,
        "head": head_direction,
        "attention": attention_score,
        "attention_status": attention_status,
        "breathing": breathing_rate,
        "yawn": yawn_count,
        "emotion": emotion,
        "fatigue": fatigue_score,
        "fatigue_level": fatigue_level,
        "recommendation": health_recommendation,
       
        
    })