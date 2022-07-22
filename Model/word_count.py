import string
from nltk.corpus import stopwords
import database as db

mydb = db.connect()
mycursor = mydb.cursor()
sql = "select question from qa_pairs union select answer from qa_pairs"

mycursor.execute(sql)

word_counts = dict()
alphabet = "abcdefghijklmnopqrstuvwxyz"
stop_words = set(stopwords.words('english'))

buffer = ''
for question in mycursor:
    question_lower_case = question[0].lower()
    print("Dealing with " + question_lower_case)
    for i in range(len(question_lower_case)):
        if (question_lower_case[i] in alphabet or question_lower_case[i] == "'"):
            buffer += question_lower_case[i]
        else:
            if len(buffer) > 0 and buffer not in stop_words:
                if buffer in word_counts.keys():
                    word_counts[buffer] += 1
                else:
                    word_counts[buffer] = 1   
            buffer = ''

with open("word_counts.txt", "w") as f:
    for word_count in word_counts:
        f.writelines(word_count + " " + str(word_counts[word_count]) +'\n')