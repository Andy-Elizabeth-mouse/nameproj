import torch as th
import torch.nn as nn
import torch.optim as optim

class NameVerifierModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(NameVerifierModel, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=4500, embedding_dim=input_size)
        self.hidden = nn.Linear(input_size * 2, hidden_size)
        self.relu = nn.ReLU()
        self.output = nn.Linear(hidden_size, 2)
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.embedding(x).view(1, -1)
        x = self.hidden(x)
        x = self.relu(x)
        x = self.output(x)
        x = self.softmax(x)
        return x

def get_data(path="nameproj/name_verifier/data.csv", _char2index={}):
    data = []
    char2index = _char2index
    with open(path, "r", encoding="utf8") as f:
        f.readline()
        for line in f:
            name, label = line.strip().split(",")
            
            for char in name:
                if char not in char2index:
                    char2index[char] = len(char2index)
            
            name_idx = [char2index[char] for char in name]
            data.append((name_idx, int(label)))
    return data, char2index, dict((v, k) for k, v in char2index.items())

def train():
    data, char2index, index2char = get_data()
    model = NameVerifierModel(input_size=128, hidden_size=1024).cuda()
    criterion = nn.BCELoss().cuda()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(1):
        for i, (name, label) in enumerate(data):
            name = th.tensor(name, dtype=th.long).cuda()
            label = th.tensor([label==0, label==1], dtype=th.float).cuda()
            
            optimizer.zero_grad()
            with th.autocast("cuda"):
                output = model(name).view(2)
            loss = criterion(output.to(th.float).clamp(0 + 1e-6, 1 - 1e-6), label.clamp(0 + 1e-6, 1 - 1e-6))
            loss.backward()
            optimizer.step()
            
            if i % 100 == 0:
                print(f"\rEpoch {epoch}, Iteration {i}, Loss {loss.item()}      ", end="")
        print()
    
    th.save(model.state_dict(), "nameproj/name_verifier/model.pth")
    th.save(char2index, "nameproj/name_verifier/char2index.pth")
    th.save(index2char, "nameproj/name_verifier/index2char.pth")

if __name__ == "__main__":
    th.backends.cudnn.enable = True
    th.backends.cudnn.benchmark = True
    train()
