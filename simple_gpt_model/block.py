import torch
import torch.nn as nn
from torch.nn import functional as F

from feed_fwd import FeedForward
from multi_head_attention import MultiHeadAttention
from constants import *

class Block(nn.Module):
    """ Transformer block: communication followed by computation """
    def __init__(self,use_kv_cache=False):
        super().__init__()
        # 1. First Normalization Layer
        self.pre_attention_norm = nn.LayerNorm(n_embd)

        # 2. Communication (Multi-Head Attention)
        self.sa = MultiHeadAttention(use_kv_cache)

        # 3. Second Normalization Layer
        self.post_attention_norm = nn.LayerNorm(n_embd)

        # 4. Computation (Feed-Forward)
        self.ffwd = FeedForward()

    def forward(self, x):
        print(f"Block.forward received x.shape: {x.shape}")

        # Notice the Residual Connections (x + ...)
        # Also notice we apply Norm BEFORE the layer (Pre-Norm formulation)
        # Step 1: Attention
        pre_attention_norm_applied = self.pre_attention_norm(x)
        x = x + self.sa(pre_attention_norm_applied)

        # Step 2: Feed-Forward
        post_attention_norm_applied = self.post_attention_norm(x)
        out = x + self.ffwd(post_attention_norm_applied)
        return out

if __name__ == "__main__":    # Create the model
  block = Block()
  #breakpoint()

  # Random numbers from 0 to 9. of shape (batch, tokens, embedding-size)
  input = torch.randint(10, (1, 5, n_embd)).float()
  out = block(input)
  print(f'out: {out}')
  print(f'out.shape: {out.shape}')
