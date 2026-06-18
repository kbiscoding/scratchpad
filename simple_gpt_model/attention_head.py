import torch
import torch.nn as nn
from torch.nn import functional as F

from constants import *


class Head(nn.Module):
    """ One head of self-attention """
    def __init__(self):
        super().__init__()

        # 1. The Projections (Linear Layers without bias usually)
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        # 2. The Triangular Mask (Buffer = Not a trainable parameter)
        # We create a large mask (e.g., 1000x1000) and slice it later

        # register_buffer is used for fields which are part of model but NOT trained.
        # It will automatically move to GPU if .cuda() is used
        # self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        # without register_buffer, you are telling that it should be trained
        # It has to be explicitly moved to GPU if .cuda() is used
        self.tril = torch.tril(torch.ones(block_size, block_size))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        print(f"Head.forward received x.shape: {x.shape}")
        # Input shape: (Batch, Time, Channels/Embedding)
        B, T, C = x.shape
        # 1. Calculate Q, K, V
        k = self.key(x) # (B, T, head_size)
        q = self.query(x) # (B, T, head_size)
        # 2. Compute Attention Scores (Affinities)
        # Equation: (Q @ K_transpose) / sqrt(d_k)
        # Transpose the last two dimensions of K to match Q
        weights = q @ k.transpose(-2,-1) * (head_size ** -0.5) # (B, T, T)
        # 3. Apply the Mask (The "Decoder" property)
        # Wherever the mask is 0, set weightsght to -infinity
        weights = weights.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        # 4. Softmax
        weights = F.softmax(weights, dim=-1) # (B, T, T)
        
        weights = self.dropout(weights)
        # 5. Aggregate Values
        v = self.value(x) # (B, T, head_size)
        out = weights @ v # (B, T, T) @ (B, T, head_size) -> (B, T,head_size)
        return out
    


if __name__ == "__main__":    # Create the model
  head = Head()

  # Random numbers from 0 to 9. of shape (batch, tokens, embedding-size)
  input = torch.randint(10, (1, 5, n_embd)).float()
  out = head(input)
  print(f'out: {out}')
  print(f'out.shape: {out.shape}')  
