import mglearn
import numpy as np
from sklearn.datasets import load_files
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from Introduction_to_Machine_Learning_with_Python.utils import resource_path

reviews_train = load_files(resource_path('aclImdb', 'train'))
text_train, y_train = reviews_train.data[:1200], reviews_train.target[:1200]
reviews_test = load_files(resource_path('aclImdb', 'test'))
text_test, y_test = reviews_test.data[:400], reviews_test.target[:400]

vect = CountVectorizer(max_features=10000, max_df=.15)
X = vect.fit_transform(text_train)
lda = LatentDirichletAllocation(n_topics=10, learning_method="batch", max_iter=25, random_state=0)
document_topics = lda.fit_transform(X)

sorting = np.argsort(lda.components_, axis=1)[:, ::-1]
feature_names = np.array(vect.get_feature_names())
mglearn.tools.print_topics(topics=range(10), feature_names=feature_names, sorting=sorting, topics_per_chunk=5, n_words=10)