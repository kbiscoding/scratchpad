import torch
import torch.nn as nn
from torch.nn import functional as F
class BigramLanguageModel(nn.Module):
def __init__(self, vocab_size):
super().__init__()
# Each token directly reads off the logits for the next token from

a lookup table
# Table size: [65 x 65]
self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)
def forward(self, idx, targets=None):
# idx and targets are both (B, T) tensor of integers
# 1. Look up the logits
# "Logits" are the raw, unnormalized scores for the next character
logits = self.token_embedding_table(idx) # Shape: (B, T, C) ->

(Batch, Time, Channels/Vocab)
if targets is None:
loss = None
else:
# 2. Reshape for Cross Entropy
# PyTorch Cross_Entropy expects (Batch*Time, Vocab_Size)
B, T, C = logits.shape
logits = logits.view(B*T, C)
targets = targets.view(B*T)
# 3. Calculate Loss
# Compare the guess (logits) with the answer (targets)

loss = F.cross_entropy(logits, targets)
return logits, loss
def generate(self, idx, max_new_tokens):
# idx is (B, T) array of indices in the current context
for _ in range(max_new_tokens):
# 1. Get the predictions
logits, loss = self(idx)
# 2. Focus only on the last time step
# We only care about the very last character to predict what

comes NEXT

logits = logits[:, -1, :] # Becomes (B, C)
# 3. Apply Softmax to get probabilities
probs = F.softmax(logits, dim=-1) # (B, C)
# 4. Sample from the distribution
# Instead of just picking the highest (argmax), we sample to

get variety

idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
# 5. Append sampled index to the running sequence
idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
return idx