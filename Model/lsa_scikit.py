import sklearn
# Import all of the scikit learn stuff
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
from nltk.corpus import stopwords
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas", lineno=570)

question1 = 'Roman Abramovich is the owner of Chelsea football club and various other high-value assets in the United Kingdom. He is a person of interest to the Home Office because of his links to the Russian state and his public association with corrupt activities and practices. Last week, the Prime Minister said that Abramovich is facing sanctions, but he later corrected the record to say that he is not. Why on earth is he not facing sanctions?'
question2 = 'Last September, my constituent Dylan Rich, who was a talented 17-year-old footballer, tragically collapsed and died during a youth FA cup game. His family and his club, the West Bridgford Colts, raised money in his honour to buy more defibrillators to put on-site, but were faced with a VAT bill of hundreds of pounds on each life-saving device. Will my right hon. Friend commit to reviewing the VAT on commercial defibrillators to bring them in line with the zero rate applied to other medical instruments, and will he meet me, Dylan’s family and his club to discuss this much-needed change? '
question3 = 'The nurses and doctors working at Warrington Hospital in my constituency provide selfless care for families living in some of the most deprived areas of England, where life expectancy is 12 years lower than the national average. At the same time, the population has expanded, with thousands of new homes being built in Warrington and putting pressure on services, particularly at the general hospital. Does the Prime Minister agree that tackling health inequalities is key to levelling up, and will he support my campaign for a new hospital in Warrington?'
question4 = 'The situation in Ukraine continues to appal most of the world and shame the rest—and, importantly, highlights the need to break our economic dependency both on Russia and on China. Does the Prime Minister agree that our national security must be protected, and our food, energy, fibre and national infrastructure must be secure, both now and in the future, from hostile Governments? Specifically, will he commit to the real hydrogen strategy that both industry and trade unions such as the GMB are calling for by doubling the hydrogen production target for 2030?'

texts = []
texts.append(question1)
texts.append(question2)
texts.append(question3)
texts.append(question4)

# stop_words = set(stopwords.words('english'))
# stop_words.update(['Prime', 'Minister', 'right', 'hon.', 'Gentleman'])

# vectorizer = CountVectorizer(min_df=1, stop_words=stop_words)
# dtm = vectorizer.fit_transform(texts)

vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
bag_of_words = vectorizer.fit_transform(texts)

svd = TruncatedSVD(n_components=2)
lsa = svd.fit_transform(bag_of_words)

topic_encoded_df = pd.DataFrame(lsa, columns=["topic_1", "topic_2"])
topic_encoded_df['texts'] = texts
# print(topic_encoded_df[["texts", "topic_1", "topic_2"]])

dictionary = vectorizer.get_feature_names()
# print(dictionary)

encoding_matrix = pd.DataFrame(svd.components_, index=['topic_1', 'topic_2']).T
encoding_matrix["terms"] = dictionary
# print(encoding_matrix)

encoding_matrix['abs_topic_1'] = np.abs(encoding_matrix['topic_1'])
encoding_matrix['abs_topic_2'] = np.abs(encoding_matrix['topic_2'])

encoding_matrix = encoding_matrix.sort_values('abs_topic_2', ascending=False)
print(encoding_matrix)

# lsa = TruncatedSVD(2, algorithm = 'arpack')
# dtm_lsa = lsa.fit_transform(dtm.asfptype())
# dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)

# print(pd.DataFrame(lsa.components_,index=["component_1","component_2"],columns = vectorizer.get_feature_names()))

# print(pd.DataFrame(dtm_lsa, index = texts, columns = ["component_1","component_2"]))