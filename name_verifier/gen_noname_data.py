import random

# 获取是名的字符串
names = set()
with open("nameproj/name_verifier/name1.txt", "r", encoding="utf8") as f:
    for line in f:
        names.add(line.strip())
with open("nameproj/name_verifier/name2.txt", "r", encoding="utf8") as f:
    for line in f:
        names.add(line.strip())

# 获取汉字常用字表
common_used_hanzi = set()
with open("nameproj/chinesename/chinesename/source/firstnames.txt", "r", encoding="utf8") as f:
    for line in f:
        for item in line.strip().split():
            common_used_hanzi.add(item)
common_used_hanzi = list(common_used_hanzi)

# 生成非名的字符串
nonames = []
for i in range(19465):
    name = names.__iter__().__next__()
    while name in names:
        name = ""
        for j in range(2):
            name += random.choice(common_used_hanzi)[0]
    nonames.append(name)

# 保存
with open("nameproj/noname2.txt", "w", encoding="utf8") as f:
    for name in nonames:
        f.write(name + "\n")

