from gensim import corpora, matutils
from gensim.models import LdaModel
# from gensim.models import LsiModel
import string_split
import numpy as np
import math

# If KeyBERT is being used
from keybert import KeyBERT
from nltk.corpus import stopwords

import sys
sys.path.append("..")
import database as db

# model = LsiModel.load("lsi.model")
model = LdaModel.load("lda.model")
dictionary = corpora.Dictionary.load("dictionary")

mydb = db.connect()
mycursor = mydb.cursor(buffered=True)
select = "select * from qa_pairs"
# select = "select * from qa_pairs inner join pmq_evaluation on qa_pairs.id = pmq_evaluation.qa_pair_id"

mycursor.execute(select)
updates = list()

# If KeyBERT is used...
stop_words = set(stopwords.words('english'))
additional = list()

with open("../Model/pmq_stop_words.txt", "r") as f:
        for line in f.readlines():
            additional.append(line.strip())

stop_words.update(additional)
kw_model = KeyBERT()

for row in mycursor:
    index = row[0]
    question = row[1]
    answer = row[3]
    answer_relevance = row[6]
    
    # For KeyBERT
    question_keywords = kw_model.extract_keywords(question, stop_words=stop_words, top_n=2)
    answer_keywords = kw_model.extract_keywords(answer, stop_words=stop_words, top_n=2)
    
    question_split = list()
    for keyword in question_keywords:
        question_split.append(keyword[0])

    answer_split = list()
    for keyword in answer_keywords:
        answer_split.append(keyword[0])
    
    # When Not Using KeyBERT
    # question_split = string_split.split_contribution(question.lower(), "pmq_stop_words.txt")
    # answer_split = string_split.split_contribution(answer.lower(), "pmq_stop_words.txt")
    
    print(index)
    question_bow = dictionary.doc2bow(question_split)
    answer_bow = dictionary.doc2bow(answer_split)
        
    question_lsi = model[question_bow]
    answer_lsi = model[answer_bow]

    c = matutils.sparse2full(question_lsi, 300)
    d = matutils.sparse2full(answer_lsi, 300)
    
    dot_product = np.dot(c, d)
    norm_c = np.linalg.norm(c)
    norm_d = np.linalg.norm(d)  
    sim = dot_product / (norm_c * norm_d)
    if sim < 0:
        sim = 0
    
    updates.append((index, round(sim, 4)))
    
mydb = db.connect()
mycursor = mydb.cursor(buffered=True)

for row in updates:
    print(row[0])
    try:
        update = "update qa_pairs set answer_relevance = " + str(row[1]) + " where id = " + str(row[0]) + ";"
        # update = "update pmq_evaluation set std_lda_n1 = " + str(row[1]) + " where qa_pair_id = " + str(row[0]) + ";"
        mycursor.execute(update)
        mydb.commit()
    except:
        # update = "update pmq_evaluation set std_lsi_n5 = 1 where qa_pair_id = " + str(row[0]) + ";"
        update = "update qa_pairs set answer_relevance = 0.5 where id = " + str(row[0]) + ";"
        mycursor.execute(update)
        mydb.commit()

mycursor.close()
mydb.close()