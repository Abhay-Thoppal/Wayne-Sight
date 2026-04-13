import os
import numpy as np

DATA_PATH = "dataset"

X = []
y = []

labels = os.listdir(DATA_PATH)

for idx, label in enumerate(labels):
    folder = os.path.join(DATA_PATH, label)

    for file in os.listdir(folder):
        data = np.load(os.path.join(folder, file))
        X.append(data)
        y.append(idx)

# X = np.array(X)
# y = np.array(y)
#
# print("X shape:", X.shape)  # (samples, 30, 63)
# print("y shape:", y.shape)