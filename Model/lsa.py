import gensim
import nltk
from gensim import corpora, models, similarities
from gensim.models import LsiModel
from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from nltk.corpus import stopwords
import time

def remove_stop_words(sentence, stop_words):
    filtered = []
    for word in sentence:
        if word not in stop_words:
            filtered.append(word)
    return filtered


stop_words = set(stopwords.words('english'))
stop_words.update(['Prime', 'Minister', 'right', 'hon.', 'Gentleman'])

question1 = 'Roman Abramovich is the owner of Chelsea football club and various other high-value assets in the United Kingdom. He is a person of interest to the Home Office because of his links to the Russian state and his public association with corrupt activities and practices. Last week, the Prime Minister said that Abramovich is facing sanctions, but he later corrected the record to say that he is not. Why on earth is he not facing sanctions?'
question2 = 'Last September, my constituent Dylan Rich, who was a talented 17-year-old footballer, tragically collapsed and died during a youth FA cup game. His family and his club, the West Bridgford Colts, raised money in his honour to buy more defibrillators to put on-site, but were faced with a VAT bill of hundreds of pounds on each life-saving device. Will my right hon. Friend commit to reviewing the VAT on commercial defibrillators to bring them in line with the zero rate applied to other medical instruments, and will he meet me, Dylan’s family and his club to discuss this much-needed change? '
question3 = 'The nurses and doctors working at Warrington Hospital in my constituency provide selfless care for families living in some of the most deprived areas of England, where life expectancy is 12 years lower than the national average. At the same time, the population has expanded, with thousands of new homes being built in Warrington and putting pressure on services, particularly at the general hospital. Does the Prime Minister agree that tackling health inequalities is key to levelling up, and will he support my campaign for a new hospital in Warrington?'
question4 = 'The situation in Ukraine continues to appal most of the world and shame the rest—and, importantly, highlights the need to break our economic dependency both on Russia and on China. Does the Prime Minister agree that our national security must be protected, and our food, energy, fibre and national infrastructure must be secure, both now and in the future, from hostile Governments? Specifically, will he commit to the real hydrogen strategy that both industry and trade unions such as the GMB are calling for by doubling the hydrogen production target for 2030?'

texts = []
texts.append(remove_stop_words(question1.lower().split(), stop_words))
texts.append(remove_stop_words(question2.lower().split(), stop_words))
texts.append(remove_stop_words(question3.lower().split(), stop_words))
texts.append(remove_stop_words(question4.lower().split(), stop_words))

dictionary = corpora.Dictionary(texts)
print(type(dictionary))
corpus = [dictionary.doc2bow(text) for text in texts]
print(type(corpus))

# lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=20)
# lsi.save("lsi.model")

lsi = LsiModel.load("lsi.model")
answer = "It is not appropriate for me to comment on individual cases at this stage, but I stand by what I said in the House and what we put on the record. Be in no doubt that the actions that we and this House have already taken are having an effect in Moscow. By exposing the ownership of properties and companies in the way we are, and by sanctioning 275 individuals already and a further 100 last week, the impact is being felt. In addition, we will publish a full list of all those associated with the Putin regime, and of course we have already sanctions on Putin and Lavrov themselves. The House will have heard what the President of the United States had to say last night. The vice is tightening on the Putin regime, and it will continue to tighten."

vec_bow = dictionary.doc2bow(answer.lower().split())
vec_lsi = lsi[vec_bow]
index = similarities.MatrixSimilarity(lsi[corpus])
print(index[vec_lsi])


# 2 topics = 0.65, 0.98, 0.82, 0.89
# 3 topics = 0.21, 0.95, 0.64, 0.88
# 4 topics = 0.13, 0.83, 0.53, 0.64
# etc