import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import torch
import torch.nn as nn
import threading
from queue import Queue


speech_queue = Queue()
def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("Speech error:", e)
        speech_queue.task_done()


class GestureModel(nn.Module):
    def __init__(self, input_size=63, hidden_size=128, num_classes=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out


labels = ["Hello", "Where"]
model = GestureModel(num_classes=len(labels))

model.load_state_dict(torch.load("gesture_model.pt", weights_only=True))
model.eval()

print(torch.cuda.is_available())
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()


cap = cv2.VideoCapture(0)

sequence = []
SEQUENCE_LENGTH = 5

predictions = []
SMOOTHING_WINDOW = 2

sentence = []
last_added_word = None

cooldown_counter = 0
COOLDOWN_FRAMES = 10

engine = pyttsx3.init()
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

while cap.isOpened():
    ret, frame = cap.read()
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

            scale = np.linalg.norm([
                hand_landmarks.landmark[12].x - base_x,
                hand_landmarks.landmark[12].y - base_y,
                hand_landmarks.landmark[12].z - base_z
            ])

            landmarks = []

            for lm in hand_landmarks.landmark:
                landmarks.extend([
                    (lm.x - base_x) / scale,
                    (lm.y - base_y) / scale,
                    (lm.z - base_z) / scale
                ])

            sequence.append(landmarks)
            if len(sequence) > SEQUENCE_LENGTH:
                sequence.pop(0)

            if len(sequence) == SEQUENCE_LENGTH:
                input_data = torch.tensor([sequence], dtype=torch.float32).to(device)

                with torch.no_grad():
                    output = model(input_data)
                    pred = torch.argmax(output, dim=1).item()

                probs = torch.softmax(output, dim=1)
                confidence = probs[0][pred].item()

                cv2.putText(frame, f"Confidence: {confidence:.2f}, raw: {labels[pred]}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                if confidence > 0.7:
                    predictions.append(pred)

                    if len(predictions) > SMOOTHING_WINDOW:
                        predictions.pop(0)

                    final_pred = max(set(predictions), key=predictions.count)
                    label = labels[final_pred]
                else:
                    label = label if 'label' in locals() else "..."

                if confidence > 0.7:
                    if label != last_added_word and cooldown_counter == 0:
                        sentence.append(label)
                        last_added_word = label
                        cooldown_counter = COOLDOWN_FRAMES

                        if speech_queue.qsize() < 2:
                            speech_queue.put(label)

                if cooldown_counter > 0:
                    cooldown_counter -= 1

                cv2.putText(frame, f"Prediction: {label}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, "Sentence: " + " ".join(sentence), (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("WayneSight Inference", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()