from gensim import corpora, models
from gensim.models import LsiModel
# from gensim.models import LdaModel
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
    words = string_split.split_contribution(lowercase_contribution, "pmq_stop_words.txt")
    print(words)
    contributions.append(words)

print("Getting dictionary")
dictionary = corpora.Dictionary(contributions)

print("Getting corpus")
corpus = [dictionary.doc2bow(contribution, allow_update=True) for contribution in contributions]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

print("Getting model")
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
# lda = LdaModel(corpus_tfidf, num_topics=300)

print("Saving the model and dictionary")
lsi.save("lsi.model")
# lda.save("lda.model")
dictionary.save("dictionary")
