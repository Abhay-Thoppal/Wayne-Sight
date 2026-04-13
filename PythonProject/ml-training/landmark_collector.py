import cv2
import mediapipe as mp
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

camera_feed = cv2.VideoCapture(0)

SEQUENCE_LENGTH = 30
gesture_name = "Where"

save_path = f"dataset/{gesture_name}"
os.makedirs(save_path, exist_ok=True)

recording = False
sequence = []
sample_count = len(os.listdir(save_path))

while camera_feed.isOpened():
    ret, frame = camera_feed.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            base_x = hand_landmarks.landmark[0].x
            base_y = hand_landmarks.landmark[0].y
            base_z = hand_landmarks.landmark[0].z
            landmarks = []

            scale = np.linalg.norm([
                hand_landmarks.landmark[12].x - base_x,
                hand_landmarks.landmark[12].y - base_y,
                hand_landmarks.landmark[12].z - base_z
            ])

            for lm in hand_landmarks.landmark:
                landmarks.extend([
                    (lm.x - base_x) / scale,
                    (lm.y - base_y) / scale,
                    (lm.z - base_z) / scale
                ])

            sequence.append(landmarks)

    cv2.putText(frame, f"Recording: {recording}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Frames: {len(sequence)}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("WayneSight Recorder", frame)

    key = cv2.waitKey(1)

    if key == ord('r'):
        print("Recording started")
        recording = True
        sequence = []

    if recording:
        if len(sequence) == SEQUENCE_LENGTH:
            sample_count += 1
            file_path = os.path.join(save_path, f"sample_{sample_count}.npy")
            np.save(file_path, np.array(sequence))
            recording = False
            print(f"Saved: {file_path}")

    if key == ord("q"):
        break

camera_feed.release()
cv2.destroyAllWindows()

sequence = np.array(sequence)
print(sequence.shape)