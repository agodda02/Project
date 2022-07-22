from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
stop_words.update(['speaker', 'hon', 'right', 'minister', 'prime', 'friend', 'government', 'gentleman', 'house', 'mr'])

def split_contribution(lowercase_contribution):
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
