import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT = [33, 160, 158, 133, 153, 144]
RIGHT = [362, 385, 387, 263, 373, 380]


def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def EAR(landmarks, eye):
    A = distance(landmarks[eye[1]], landmarks[eye[5]])
    B = distance(landmarks[eye[2]], landmarks[eye[4]])
    C = distance(landmarks[eye[0]], landmarks[eye[3]])

    return (A + B) / (2 * C)


def detect_eyes(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if not result.multi_face_landmarks:
       return frame, False, 0, None

    face = result.multi_face_landmarks[0]

    leftEAR = EAR(face.landmark, LEFT)
    rightEAR = EAR(face.landmark, RIGHT)

    ear = (leftEAR + rightEAR) / 2

    eyes_open = ear > 0.23

    h, w, _ = frame.shape

    for id in LEFT + RIGHT:
        x = int(face.landmark[id].x * w)
        y = int(face.landmark[id].y * h)

        cv2.circle(frame, (x, y), 2, (0,255,0), -1)

    cv2.putText(
        frame,
        f"EAR:{ear:.2f}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    return frame, eyes_open, ear, face.landmark