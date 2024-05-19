import random

with open("nameproj/name_verifier/name2.txt", "r", encoding="utf8") as f1, \
     open("nameproj/name_verifier/noname2.txt", "r", encoding="utf8") as f2, \
     open("nameproj/name_verifier/name1.txt", "r", encoding="utf8") as f3, \
     open("nameproj/name_verifier/noname1.txt", "r", encoding="utf8") as f4:
    names = []
    for line in f1:
        names.append(line.strip() + ",0")
    for line in f2:
        names.append(line.strip() + ",1")
    for line in f3:
        names.append(line.strip() + ",0")
    for line in f4:
        names.append(line.strip() + ",1")
    random.shuffle(names)
    with open("nameproj/name_verifier/data.csv", "w", encoding="utf8") as f:
        f.write("name,label\n")
        for name in names:
            f.write(name + "\n")