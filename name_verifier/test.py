from train import NameVerifierModel, get_data
import torch as th

def test():
    char2index = th.load("nameproj/name_verifier/char2index.pth")
    data, _, _ = get_data("nameproj/name_verifier/data2.csv", char2index)
    model = NameVerifierModel(input_size=128, hidden_size=1024).cuda()
    model.load_state_dict(th.load("nameproj/name_verifier/model.pth"))
    
    correct = 0
    total = 0
    with th.no_grad():
        for _, (name, label) in enumerate(data):
            name = th.tensor(name, dtype=th.long).cuda()
            label = th.tensor([label==0, label==1], dtype=th.float).cuda()
            
            output = model(name).view(2)
            if th.argmax(output) == th.argmax(label):
                correct += 1
            total += 1
            print(f"\rAccuracy: {correct / total:.2f}", end="")

if __name__ == "__main__":
    test()
