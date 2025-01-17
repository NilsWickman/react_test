import torch
from torch import nn

torch.manual_seed(0)
device = "cpu"

print(f"Using {device} device")

class FIR_model(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(6*7, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 7)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def retreive_AI ():
    model = FIR_model().to(device)
    return model