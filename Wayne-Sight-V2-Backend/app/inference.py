import torch
from app.model import GestureModel

labels = ["hello", "where"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = GestureModel(num_classes=len(labels))
model.load_state_dict(torch.load("gesture_model.pt", weights_only=True))
model.eval()
model.to(device)


def predict(sequence):
    input_data = torch.tensor([sequence], dtype=torch.float32).to(device)

    with torch.no_grad():
        output = model(input_data)
        pred = torch.argmax(output, dim=1).item()

    probs = torch.softmax(output, dim=1)
    confidence = probs[0][pred].item()

    return labels[pred], float(confidence)