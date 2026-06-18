import torch
import torch.nn as nn
from torch.nn import functional as F

from block import Block
from constants import *

class GPTLanguageModel(nn.Module):
    def __init__(self, vocab_size, use_kv_cache=False):
        super().__init__()
        # 1. Embeddings
        # Token embeddings (Words)
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        # Position embeddings for positions (0, 1, 2...). 
        self.position_embedding_table = nn.Embedding(block_size, n_embd) # Positions x n_embed
        # 2. The Transformer Blocks (The "Brain")
        # We stack 4 blocks
        self.blocks = nn.Sequential(
        Block(use_kv_cache),
        Block(use_kv_cache),
        Block(use_kv_cache),
        nn.LayerNorm(n_embd), # Final normalization
        )
        
        # Each layer emits (batch, tokens, n_embed). Layernorm maintains those dimensions
        # lmhead converts it to probability for each readable vocabulary.

        # 3. The Language Model Head (Final projection to vocabulary)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        print(f"GPTLanguageModel.forward received idx.shape: {idx.shape}")        
        B, T = idx.shape
        # 1. Create Embeddings
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device="cpu")) # (T,C)
        x = tok_emb + pos_emb # (B,T,C) -> Combine Meaning + Position
        # 2. Run through Transformer Blocks
        x = self.blocks(x) # (B,T,C)
        # 3. Project to Vocabulary
        logits = self.lm_head(x) # (B,T,vocab_size)
        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        return logits, loss

    def generate(self, idx, max_new_tokens):
        print(f"GPTLanguageModel.generate received idx.shape: {idx.shape}")        
        # (Same generation logic as Bigram model)
        for _ in range(max_new_tokens):
            # Crop context if it gets too long (we can only see 'block_size' back)
            idx_cond = idx[:, -block_size:]
            logits, loss = self(idx_cond)   # logits is      (batch, existing tokens, vocab size). It signifies what is the prediction based on each token
            logits = logits[:, -1, :]       # logits becomes (batch, 1, vocab size). It signifies what is the prediction based on just the last token.
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)  # (1, 1)
            idx = torch.cat((idx, idx_next), dim=1)             # (1, accumulated token ids)
        return idx

    def generate_for_inference(self, idx, max_new_tokens):
        print(f"GPTLanguageModel.generate_for_inference received idx.shape: {idx.shape}")
        out = idx
        # (Same generation logic as Bigram model)
        # for _ in range(max_new_tokens):
        for _target_token in range(max_new_tokens):
            print(f"target_token: [{_target_token + 1}] (as index)")
            # Crop context if it gets too long (we can only see 'block_size' back)
            idx_cond = idx[:, -block_size:]
            logits, loss = self(idx_cond)   # logits is      (batch, existing tokens, vocab size). It signifies what is the prediction based on each token
            logits = logits[:, -1, :]       # logits becomes (batch, 1, vocab size). It signifies what is the prediction based on just the last token.
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)  # (1, 1)

            # DO NOT carry forward previos idx for inference
            idx = idx_next

            # Accumulate only for output, not for running inference loops.
            out = torch.cat((out, idx_next), dim=1)             # (1, accumulated token ids)
            print(f"GPTLanguageModel.generate_for_inference: idx_next {idx_next} cumulative: {out}")
        return out

# Dummy decode function
def decode(tokens):
    return " ".join(str(t) for t in tokens)

# The main is copy pasted from BigramLanguageModel
if __name__ == "__main__":    # Create the model
    vocab_size = 5
    
    # # ✅ Create proper dummy batch (B=1, T=3)
    # x = torch.randint(vocab_size, (1, 3))
    # y = torch.randint(vocab_size, (1, 3))

    # print(f'x: {x}')
    # print(f'y: {y}')

    m = GPTLanguageModel(vocab_size, use_kv_cache=False)
    # breakpoint()
    # logits, loss = m(x, y) # Run one batch just to check shape
    # print(f"logits: {logits}")
    # print(f"Initial Loss: {loss.item()}")
    # Expected Loss: -ln(1/65) ≈ 4.17. If it's near 4.17, the math is working.
    # Generate Text (Untrained)
    # We start with a single zero (newline character) as context
    context = torch.zeros((1, 1), dtype=torch.long)

    # Training mode can be done with or without KV cache, but if done with KV cache, it is wrong.
    # That is because for training you need full Q. In inference mode, Q from last token is enough.
    print("[Training  mode, full QKV]Decoded output:" + decode(m.generate(context, max_new_tokens=10)[0].tolist()))

    # Inference can be done with or without KV cache
    # print("[Inference mode, KV Cache]Decoded output:" + decode(m.generate_for_inference(context, max_new_tokens=10)[0].tolist())) 
