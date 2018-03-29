import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline

from Introduction_to_Machine_Learning_with_Python.utils import resource_path

reviews_train = load_files(resource_path('aclImdb', 'train'))
text_train, y_train = reviews_train.data[:1200], reviews_train.target[:1200]
reviews_test = load_files(resource_path('aclImdb', 'test'))
text_test, y_test = reviews_test.data[:400], reviews_test.target[:400]

vect = CountVectorizer().fit(text_train)
X_train = vect.transform(text_train)
X_test = vect.transform(text_test)

scores = cross_val_score(LogisticRegression(), X_train, y_train, cv=5)
print(np.mean(scores))

param_grid = {'C': [0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid.fit(X_train, y_train)
print("best score: {:.2f}".format(grid.best_score_))
print("best params: ", grid.best_params_)

print("Score for test: {:.2f}".format(grid.score(X_test, y_test)))

# С помощью параметра min_df мы можем задать минимальное количество документов, в котором должен появиться токен
vect = CountVectorizer(min_df=5).fit(text_train)
X_train = vect.transform(text_train)
X_test = vect.transform(text_test)

log = LogisticRegression(C=0.001).fit(X_train, y_train)
print(log.score(X_test, y_test))

# С помощью stop_words можно удалить часто встречающиеся слова
# Как правило, фиксированные списки могут быть полезны при работе с небольшими наборами данных.
# Небольшие наборы данных не имеют достаточного объема информации, позволяющего модели самостоятельно определить,
# какие слова являются стоп-словами.
# vect = CountVectorizer(min_df=5, stop_words="english").fit(text_train)
# X_train = vect.transform(text_train)

# Масштабирование данных с помощью tf-idf
# When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold.
pipe = make_pipeline(TfidfVectorizer(min_df=5, norm=None), LogisticRegression())
param_grid = {'logisticregression__C': [0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(pipe, param_grid, cv=5)
grid.fit(text_train, y_train)
print("Best score: {:.2f}".format(grid.best_score_))

# n-grams
# cv = CountVectorizer(ngram_range=(2, 2)).fit(bards_words)
pipe = make_pipeline(TfidfVectorizer(min_df=5), LogisticRegression())
param_grid = {"logisticregression__C": [0.001, 0.01, 0.1, 1, 10, 100],
              "tfidfvectorizer__ngram_range": [(1, 1), (1, 2), (1, 3)]}
grid = GridSearchCV(pipe, param_grid, cv=5)
grid.fit(text_train, y_train)
print("Best score n-grams: {:.2f}".format(grid.best_score_))
print("Best params n-grams: \n{}".format(grid.best_params_))
