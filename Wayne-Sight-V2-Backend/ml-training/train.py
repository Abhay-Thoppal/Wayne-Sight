import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from model import GestureModel
from sklearn.model_selection import train_test_split


DATA_PATH = "dataset"

labels = os.listdir(DATA_PATH)
model = GestureModel(num_classes=len(labels))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"THIS IS THE DEVICE!!!! {labels}")
model = model.to(device)

X = []
y = []

for idx, label in enumerate(labels):
    folder = os.path.join(DATA_PATH, label)

    for file in os.listdir(folder):
        data = np.load(os.path.join(folder, file))
        X.append(data)
        y.append(idx)

model = model.to(device)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
y_train = torch.tensor(y_train, dtype=torch.long).to(device)

X_val = torch.tensor(X_val, dtype=torch.float32).to(device)
y_val = torch.tensor(y_val, dtype=torch.long).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

best_val_loss = float("inf")
for epoch in range(30):
    model.train()
    optimizer.zero_grad()

    outputs = model(X_train)
    loss = criterion(outputs, y_train)

    print(outputs.device)

    loss.backward()
    optimizer.step()

    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val)
        val_loss = criterion(val_outputs, y_val)

    print(f"Epoch {epoch+1}, Train Loss: {loss.item()}, Val Loss: {val_loss.item()}")
    if val_loss.item() < best_val_loss:
        best_val_loss = val_loss.item()
        torch.save(model.state_dict(), "gesture_model.pt")
        print(f"Model saved successfully at validation loss : {val_loss.item()}")