from gensim import corpora, matutils
from gensim.models import LsiModel
import string_split
import numpy as np

import sys
sys.path.append("..")
import database as db

lsi = LsiModel.load("lsi.model")
dictionary = corpora.Dictionary.load("dictionary")

mydb = db.connect()
mycursor = mydb.cursor(buffered=True)
select = "select * from qa_pairs"

mycursor.execute(select)
updates = list()

for row in mycursor:
    index = row[0]
    question = row[1]
    answer = row[3]
    answer_relevance = row[5]
    question_split = string_split.split_contribution(question.lower())
    answer_split = string_split.split_contribution(answer.lower())
    print(index)
    question_bow = dictionary.doc2bow(question_split)
    answer_bow = dictionary.doc2bow(answer_split)
    question_lsi = lsi[question_bow]
    answer_lsi = lsi[answer_bow]

    c = matutils.sparse2full(question_lsi, 400)
    d = matutils.sparse2full(answer_lsi, 400)

    try:
        sim = np.dot(c, d) / (np.linalg.norm(c) * np.linalg.norm(d))
    except:
        sim = 0
    updates.append((index, round(sim, 4)))

for row in updates:
    print(row[0])
    try:
        update = "update qa_pairs set answer_relevance = " + str(row[1]) + " where id = " + str(row[0]) + ";"
        mycursor.execute(update)
        mydb.commit()
    except:
        print("Couldn't update this row")

mycursor.close()
mydb.close()

# question = 'It is more important than ever that we seek to continue to move forward and away from violence in Northern Ireland,  and to create stability. I am sure that the Prime Minister will agree that full participation in and support for the political and democratic process by everyone, so that the politicians can address the people’s issues, is absolutely vital. In that context, and in the light of what is happening in Northern Ireland, will the Prime Minister agree to meet us to discuss the forthcoming legislation on Northern Ireland, so that we can consider measures to increase democratic participation by people in deprived communities, look at the deplorable state of the electoral register in Northern Ireland, which is in a bad state, and deal with the discrimination against elected Members of this House from Northern Ireland who play by the rules while others get money without taking their seats? All of that needs to be addressed.'
# answer = 'I would be happy to meet the right hon. Gentleman. Indeed, I have a meeting with a number of members of his party straight after Prime Minister’s questions to discuss the vital issue of ensuring that the military covenant is properly fulfilled in Northern Ireland. He made a number of points in his question. I would throw back part of the challenge to him and his party, just as I would to others in other parties, in saying that we need to build a shared future in Northern Ireland in which we break down the barriers of segregation that have been in place for many years. That is part of the challenge to take away some of the tensions that we have seen in recent days.'

# question_split = string_split.split_contribution(question.lower())
# answer_split = string_split.split_contribution(answer.lower())
# print(question_split)
# print(answer_split)

# print("Onto the questions and answers")

# vec_bow_q = dictionary.doc2bow(question_split)
# vec_bow_a = dictionary.doc2bow(answer_split)
# vec_lsi_q = lsi[vec_bow_q]
# vec_lsi_a = lsi[vec_bow_a]

# c = matutils.sparse2full(vec_lsi_q, 400)
# d = matutils.sparse2full(vec_lsi_a, 400)

# sim = np.dot(c, d) / (np.linalg.norm(c) * np.linalg.norm(d))

# print(sim)