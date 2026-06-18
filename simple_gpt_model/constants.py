# Hyperparameters
n_embd = 32 # Dimension of the character embedding
head_size = 16 # Dimension of the Key/Query/Value vectors inside this head
dropout = 0.1 # Randomly zero out neurons to prevent overfitting

block_size = 128  # maximum context length. TODO: figure.

# FOR DEBUGGING KV CACHE, TEMPORARILY USING ONLY ONE num_heads
num_heads = 4 # multihead attention
