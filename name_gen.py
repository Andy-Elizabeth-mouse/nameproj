import random as rd

from bigram.generic_singletoken_bigram import GenericSingleTokenBigramModel
from name_verifier.infer import verify
from chinesename.chinesename.source.names import lastnames

lastnames = lastnames.split()
bi = GenericSingleTokenBigramModel()

def generate(lastname=None, firstname_len=2, skip_unrecognized=False):
    assert isinstance(lastname, str) or lastname is None
    assert isinstance(firstname_len, int) and firstname_len > 0 and firstname_len < 3
    
    name = ""
    
    if lastname is None:
        lastname = rd.choice(lastnames)
    name += lastname
    
    firstname = ""
    while firstname_len > 1 and not verify(firstname, skip_unrecognized):
        firstname = bi.generate_first()
        for _ in range(firstname_len - 1):
            firstname += bi.generate_next(firstname)
    if firstname_len == 1:
        firstname = bi.generate_first()
    name += firstname
    
    return name

def generate_multiple(number, lastname=None, firstname_len=2, skip_unrecognized=False):
    assert isinstance(number, int) and number > 0
    
    names = []
    for _ in range(number):
        names.append(generate(lastname, firstname_len, skip_unrecognized))
    return names

if __name__ == "__main__":
    print(generate())
    print(generate("张", skip_unrecognized=True))
    print(generate("李", 1))
    print(generate_multiple(5))
    print(generate_multiple(5, "王", skip_unrecognized=True))
    print(generate_multiple(5, "赵", 1))
