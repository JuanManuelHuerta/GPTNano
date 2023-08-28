x

with open('input.txt','r', encoding='utf-8') as f:
    text= f.read()


print("lenght of dataset in characters: ",len(text))

chars = sorted(list(set(text)))

vocab_size=len(chars)

print(''.join(chars))
print(vocab_size)


stoi = { ch:i for i , ch in enumerate(chars)}
itos = {i:ch for i,ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

print(encode("hii there"))
print(decode(encode("hii there")))



import torch
data=torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)
print(data)


n=int(0.9*len(data))
train_data = data[:n]
val_data = data[n:]


block_size = 8
train_data[:block_size+1]
print(train_data[:block_size+1])




x=train_data[:block_size]
y=train_data[1:block_size+1]
for t in range(block_size):
    context = x[:t+1]
    target = y[t]
    print(f"when input is {context} the targe is {target}")
    

torch.manual_seed(1337)

batch_size = 4
block_size = 8


def get_batch(split):
    data = train_data if split =='train' else val_data
    ix = torch.randint(len(data)-block_size, (batch_size,))  ## These are just rndom offsets
    x = torch.stack([data[i:i+block_size] for i in ix])
    y= torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y

xb , yb = get_batch('train')

print('inputs:')
print(xb.shape)
print(xb)
print('targets:')
print(yb.shape)
print(yb)


for b in range(batch_size):
    for t in range(block_size):
        context = xb[b,:t+1]
        target = yb[b,t]
        

###


import torch
import torch.nn as nn
from torch.nn import functional as F
torch.manual_seed(1337)


class BigramLanguageModel(nn.Module):

    def __init__(self,vocab_size):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size,vocab_size)

    def forward(self, idx, targets=None):
        logits= self.token_embedding_table(idx)  #(B,T,c): Batch, by time, by channel
        if targets is None:
            loss=None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits,targets)
        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, loss =self(idx)
            logits = logits[:,-1,:]
            probs = F.softmax(logits,dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx=torch.cat((idx, idx_next), dim=1)
        return idx
    
m=BigramLanguageModel(vocab_size)
logits,loss = m(xb,yb)
print(logits.shape)
print("loss", loss)


print(decode(m.generate(idx = torch.zeros((1,1),dtype=torch.long),max_new_tokens=100)[0 ].tolist()))


optimizer = torch.optim.AdamW(m.parameters(),lr=1e-3)
batch_size = 32
for steps in range(10000):
    xb, yb = get_batch('train')
    logits, loss =m(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()
print(loss.item())



print(decode(m.generate(idx = torch.zeros((1,1),dtype=torch.long),max_new_tokens=100)[0 ].tolist()))
      





    