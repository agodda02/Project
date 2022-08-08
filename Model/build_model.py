from gensim import corpora, models
from gensim.models import LsiModel
import string_split

import sys
sys.path.append("..")
import database as db

mydb = db.connect()
mycursor = mydb.cursor()
sql = "select question from qa_pairs union select answer from qa_pairs"

mycursor.execute(sql)

contributions = list()

for rows in mycursor:
    lowercase_contribution = rows[0].lower()
    print(lowercase_contribution)
    words = string_split.split_contribution(lowercase_contribution)
    print(words)
    contributions.append(words)

print("Getting dictionary")
dictionary = corpora.Dictionary(contributions)

print("Getting corpus")
corpus = [dictionary.doc2bow(contribution, allow_update=True) for contribution in contributions]
# corpus_tfidf = models.TfidfModel(corpus, smartirs='ntc') - look at using this for improving model. Add allow_update=True in doc2bow method above

print("Getting model")
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=75)

print("Saving the model and dictionary")
lsi.save("lsi.model")
dictionary.save("dictionary")
