import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris_dataset = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris_dataset['data'], iris_dataset['target'], random_state=0
)
# iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
# grr = pd.plotting.scatter_matrix(
#     iris_dataframe,
#     c=y_train,
#     figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=.8)
# plt.show()

for i in range(1, 10):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    X_new = np.array([[5, 2.9, 1, 0.2]])
    # prediction = knn.predict(X_new)
    # print(f"Прогноз: {prediction}")
    # print(f"Спрогнозированная метка: {iris_dataset['target_names'][prediction]}")

    y_pred = knn.predict(X_test)
    print(f"Правильность на тестовом наборе n={i}: {knn.score(X_test, y_test)}")
