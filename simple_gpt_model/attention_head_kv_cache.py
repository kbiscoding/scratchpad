import torch
import torch.nn as nn
from torch.nn import functional as F

from constants import *
from attention_head import Head

class HeadWithKVCache(Head):
    """ One head of self-attention which caches K and V past values"""
    def __init__(self):
        super().__init__()    

    def forward(self, x, past_key_values=None):
        print(f"HeadWithKVCache.forward received x.shape: {x.shape}")

        # Input shape: (Batch, Time, Channels/Embedding)
        B, T, C = x.shape
               
        # 1. Calculate K, V for the CURRENT input x only
        k = self.key(x)
        v = self.value(x)
 
        # 2. If we have history, concatenate it
        if past_key_values is not None:
            self.k_past, self.v_past = self.past_key_values
            k = torch.cat((self.k_past, k), dim=1) # Append along time dimension
            v = torch.cat((self.v_past, v), dim=1)
 
        # 3. Update the cache for the next step
        past_key_values = (k, v)
        # 4. Compute Attention using the full (concatenated) K and V
        # Q only comes from the current x!
        q = self.query(x)
        weights = q @ k.transpose(-2, -1) * (head_size ** -0.5)
       
        # ... (Rest of attention) ...
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
  head = HeadWithKVCache()

  # Random numbers from 0 to 9. of shape (batch, tokens, embedding-size)
  input = torch.randint(10, (1, 5, n_embd)).float()
  out = head(input)
  print(f'out: {out}')
  print(f'out.shape: {out.shape}')  
