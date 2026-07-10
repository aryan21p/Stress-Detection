import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# Nose, Chin, Left Eye, Right Eye
LANDMARKS = [1, 152, 33, 263]


def detect_head_pose(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if not result.multi_face_landmarks:
        return frame, "No Face"

    h, w, _ = frame.shape

    face = result.multi_face_landmarks[0]

    nose = face.landmark[1]

    left = face.landmark[33]

    right = face.landmark[263]

    center = (left.x + right.x) / 2

    direction = "Center"

    if nose.x < center - 0.03:
        direction = "Left"

    elif nose.x > center + 0.03:
        direction = "Right"

    cv2.putText(
        frame,
        f"Head : {direction}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    return frame, direction