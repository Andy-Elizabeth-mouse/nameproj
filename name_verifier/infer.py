from .train import NameVerifierModel
import torch as th

model = NameVerifierModel(128, 1024).cuda()
model.load_state_dict(th.load("nameproj/name_verifier/model.pth"))

char2index = th.load("nameproj/name_verifier/char2index.pth")
index2char = dict((v, k) for k, v in char2index.items())

def verify(name, skip_unrecognized=False):
    if name == None or name == "": return False
    if skip_unrecognized and not all(char in char2index for char in name): return False
    name = th.tensor([char2index.get(char, len(char2index)) for char in name], dtype=th.long).cuda()
    output = model(name).view(2)
    return th.argmax(output).item() == 0
