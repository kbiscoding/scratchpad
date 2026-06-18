import torch
import torch.nn as nn
from torch.nn import functional as F

from attention_head import Head
from attention_head_kv_cache import HeadWithKVCache

from constants import *

class MultiHeadAttention(nn.Module):
    """ Multiple heads of self-attention in parallel """

    def __init__(self, use_kv_cache=False):
        super().__init__()
        # Create a list of independent Heads
        if use_kv_cache:
            self.heads = nn.ModuleList([HeadWithKVCache() for _ in range(num_heads)])
        else:
            self.heads = nn.ModuleList([Head() for _ in range(num_heads)])

        # Projection layer to mix the results of all heads together
        self.proj = nn.Linear(num_heads * head_size, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        print(f"MultiHeadAttention.forward received x.shape: {x.shape}")
        # 1. Run each head independently
        out = [h(x) for h in self.heads]
        # 2. Concatenate the results over the last dimension (Channels)
        # If we have 4 heads of size 8, output is size 32
        out = torch.cat(out, dim=-1)
        # 3. Apply projection
        out = self.proj(out)
        out = self.dropout(out)
        return out



if __name__ == "__main__":    # Create the model
  multi_head_attention = MultiHeadAttention()

  # Random numbers from 0 to 9. of shape (batch, tokens, embedding-size)
  input = torch.randint(10, (1, 5, n_embd)).float()
  out = multi_head_attention(input)
  print(f'out: {out}')
  print(f'out.shape: {out.shape}')
  