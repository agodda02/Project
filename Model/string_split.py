from nltk.corpus import stopwords

def split_contribution(lowercase_contribution, file):
    stop_words = set(stopwords.words('english'))
    additional = list()

    with open(file, "r") as f:
            for line in f.readlines():
                additional.append(line.strip())

    stop_words.update(additional)

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words = list()
    buffer = ''    
    for i in range(len(lowercase_contribution)):
        if (lowercase_contribution[i] in alphabet or lowercase_contribution[i] == "'"):
            buffer += lowercase_contribution[i]
        else:
            if len(buffer) > 0 and buffer not in stop_words:
                words.append(buffer)
            buffer = ''
    return words   
