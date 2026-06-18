import torch
import torch.nn as nn
from torch.nn import functional as F

class BigramLanguageModel(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        # Each token directly reads off the logits for the next token from

        # a lookup table
        # Table size: [65 x 65]
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):
        print(f"FYI: self.token_embedding_table.weight:{self.token_embedding_table.weight}")
        print(f"FYI: idx:{idx}")

        # breakpoint()
        # idx and targets are both (B, T) tensor of integers
        # 1. Look up the logits
        # "Logits" are the raw, unnormalized scores for the next character
        logits = self.token_embedding_table(idx) # Shape: (B, T, C) ->
        print(f"FYI: logits:{logits}")

        # It is python embeddings feature that it adds 'embedding size' as last dimension
        # So if idx is having 3 word indices = [1,3], the logits will be [1,3,10]
        # That is why below, when calculating loss we have to reshape logits as (dim0*dim2, dim3).

        # (Batch, Time, Channels/Vocab)
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
        print(f"FYI: self.token_embedding_table.weight:{self.token_embedding_table.weight}")
        print(f"FYI: idx:{idx}")

        # breakpoint()
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # 1. Get the predictions
            logits, loss = self(idx)
            # 2. Focus only on the last time step
            # We only care about the very last character to predict what
            # comes NEXT
            print(f"FYI: logits from forward():{logits}")

            logits = logits[:, -1, :] # Becomes (B, C): This picks just the last vector, that is logit from last idx
            # In python : means all elements, -1 means last element.
                # :  - all batches
                # -1 - the last time step
                # :  - all vocabulary logits
            print(f"FYI: logits:{logits}") 

            # 3. Apply Softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B, C)
            # dim=-1 means to apply softmax across last dimension, ie along each batch.
            # logits: [batch, embedding-size]. So dim=-1 says that prob should sum to one across each batch, ie, apply on embedding wise.
            print(f"FYI: probs:{probs}")

            # 4. Sample from the distribution
            # Instead of just picking the highest (argmax), we sample to
            # get variety

            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # This picks up next id based on probablities with some randomness.
            # element with highest probability has highest likelihood of being picked but not always the case as max(prob)
 

            # 5. Append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
            print(f'idx became: {idx}')
        return idx
    
# Dummy decode function
def decode(tokens):
    return " ".join(str(t) for t in tokens)
    
if __name__ == "__main__":    # Create the model
    # breakpoint()
    vocab_size = 5

    # # ✅ Create proper dummy batch (B=1, T=3)
    # x = torch.randint(vocab_size, (1, 3))
    # y = torch.randint(vocab_size, (1, 3))

    # print(f'x: {x}')
    # print(f'y: {y}')

    m = BigramLanguageModel(vocab_size)
    # logits, loss = m(x, y) # Run one batch just to check shape
    # print(f"logits: {logits}")
    # print(f"Initial Loss: {loss.item()}")
    # Expected Loss: -ln(1/65) ≈ 4.17. If it's near 4.17, the math is working.
    # Generate Text (Untrained)
    # We start with a single zero (newline character) as context
    context = torch.zeros((1, 1), dtype=torch.long)
    print("Decoded output:" + decode(m.generate(context, max_new_tokens=10)[0].tolist()))
