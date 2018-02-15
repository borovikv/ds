from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC

from Introduction_to_Machine_Learning_with_Python.utils import score


def cancer_dataset():
    cancer = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=1)

    score(SVC, X_train, X_test, y_train, y_test, C=100)

    for sc, kwargs in [(MinMaxScaler, {'C': 100}), (StandardScaler, {})]:
        X_test_scaled, X_train_scaled = scale(X_test, X_train, sc())
        score(SVC, X_train_scaled, X_test_scaled, y_train, y_test, **kwargs)


def scale(X_test, X_train, scaler):
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f'Shape: {X_train_scaled.shape}')
    print(f'min значение признака до масштабирования:\n {X_train.min(axis=0)}')
    print(f'max значение признака до масштабирования:\n {X_train.max(axis=0)}')
    print(f'min значение признака после масштабирования:\n {X_train_scaled.min(axis=0)}')
    print(f'max значение признака после масштабирования:\n {X_train_scaled.max(axis=0)}')
    print(f'min значение признака после масштабирования:\n {X_test_scaled.min(axis=0)}')
    print(f'max значение признака после масштабирования:\n {X_test_scaled.max(axis=0)}')

    return X_test_scaled, X_train_scaled


# cancer_dataset()
# histograms_by_features(load_breast_cancer())
plt.show()
