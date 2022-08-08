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

    c = matutils.sparse2full(question_lsi, 75)
    d = matutils.sparse2full(answer_lsi, 75)
    minx = -1
    maxx = 1

    try:
        dot_product = np.dot(c, d)
        norm_c = np.linalg.norm(c)
        norm_d = np.linalg.norm(d)       
        sim = ((dot_product / (norm_c * norm_d)) - minx)/(maxx-minx)
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