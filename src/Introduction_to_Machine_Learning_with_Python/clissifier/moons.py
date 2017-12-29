import mglearn
from matplotlib import pyplot as plt
from sklearn.datasets import make_moons
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=100, noise=0.25, random_state=3)

# plt.scatter(X[:, 0], X[:, 1], c=y)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
forest = RandomForestClassifier(n_estimators=5, random_state=2)
print(X_train)
print(y_train)
forest.fit(X_train, y_train)
predict = forest.predict(X_test)
# plt.scatter(X_test[:, 0], X_test[:, 1], c=predict, marker='+')
print(forest.score(X_test, y_test))

fig, axes = plt.subplots(2, 3, figsize=(20, 10))
for i, (ax, tree) in enumerate(zip(axes.ravel(), forest.estimators_)):
    ax.set_title(f'Дерево {i}')
    mglearn.plots.plot_tree_partition(X_train, y_train, tree, ax=ax)

mglearn.plots.plot_2d_separator(forest, X_train, fill=True, ax=axes[-1, -1], alpha=.4)
axes[-1, -1].set_title('Случайный лес')
mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)


plt.show()
