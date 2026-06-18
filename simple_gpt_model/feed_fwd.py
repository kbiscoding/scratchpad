import torch
import torch.nn as nn
from torch.nn import functional as F

from constants import *

class FeedForward(nn.Module):
    """ A simple linear layer followed by a non-linearity """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            # 1. Expand (4x is standard for GPT)
            nn.Linear(n_embd, 4 * n_embd),
            # 2. Non-linearity (ReLU)
            nn.ReLU(),
            # 3. Project back to residual pathway
            nn.Linear(4 * n_embd, n_embd),
            # 4. Dropout
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)

if __name__ == "__main__":    # Create the model
    ff = FeedForward()
    
    # int wont work, linear works on float
    input = torch.randint(10, (1, 5, n_embd)).float()
    print(f"input.shape: {input.shape}")    
    out = ff.forward(input)
    print(f"{out}")
    print(f"out.shape: {out.shape}")