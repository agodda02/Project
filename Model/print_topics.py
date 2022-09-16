from gensim import corpora, matutils
from gensim.models import LsiModel

lsi = LsiModel.load("lsi.model")
topics = lsi.print_topics(300)
for topic in topics:
    print(topic)
    
