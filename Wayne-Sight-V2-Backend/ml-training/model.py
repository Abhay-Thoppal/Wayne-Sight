import torch
import torch.nn as nn

class GestureModel(nn.Module):
    def __init__(self, input_size=63, hidden_size=128, num_classes=1):
        super().__init__()

        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out