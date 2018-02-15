import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.decomposition import NMF, PCA
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection._split import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm.classes import SVC
from sklearn.tree.tree import DecisionTreeClassifier
from sklearn.manifold import TSNE

from Introduction_to_Machine_Learning_with_Python.utils import curry, get_people


def pca_cancer():
    cancer = load_breast_cancer()
    scaler = StandardScaler()
    scaler.fit(cancer.data)
    X_scaled = scaler.transform(cancer.data)

    pca = PCA(n_components=2)
    pca.fit(X_scaled)
    X_pca = pca.transform(X_scaled)

    # print(X_scaled.shape)
    # print(X_pca.shape)
    # print(pca.components_)

    plt.scatter(X_pca[:, 0][cancer.target == 0], X_pca[:, 1][cancer.target == 0], marker='v')
    plt.scatter(X_pca[:, 0][cancer.target == 1], X_pca[:, 1][cancer.target == 1], marker='o')
    plt.matshow(pca.components_, cmap='viridis')
    plt.yticks([0, 1], ["первая компонента", "вторая компонента"])
    plt.colorbar()
    plt.xticks(range(len(cancer.feature_names)), cancer.feature_names, rotation=60, ha='left')
    plt.xlabel("характеристика")
    plt.ylabel("главная компонента")


def pca_faces():
    people, X_people, y_people = get_people()
    image_shape = people.images[0].shape
    X_train, X_test, y_train, y_test = train_test_split(X_people, y_people, stratify=y_people, random_state=0)
    # score_local(X_train, X_test, y_train, y_test)

    pca = PCA(n_components=100, whiten=True, random_state=0).fit(X_train)
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    score_local(X_train_pca, X_test_pca, y_train, y_test)
    show_(pca, image_shape)


def nmf_faces():
    people, X_people, y_people = get_people()
    image_shape = people.images[0].shape
    X_train, X_test, y_train, y_test = train_test_split(X_people, y_people, stratify=y_people, random_state=0)

    nmf = NMF(n_components=15, random_state=0).fit(X_train)
    X_train_nmf = nmf.transform(X_train)
    X_test_nmf = nmf.transform(X_test)
    show_(nmf, image_shape)
    score_local(X_train_nmf, X_test_nmf, y_train, y_test)


def score_local(X_train, X_test, y_train, y_test):
    score = curry(X_train, X_test, y_train, y_test)

    score(KNeighborsClassifier, n_neighbors=1)  # without pca: 0.23
    score(SVC)  # without pca: 0.099
    score(LogisticRegression)  # without pca: 0.535
    score(LogisticRegression, C=100)  # without pca: 0.512
    score(DecisionTreeClassifier, random_state=0)  # without pca: 0.109
    score(DecisionTreeClassifier, random_state=0, max_depth=4)  # without pca: 0.083
    # without pca: 0.025
    score(MLPClassifier, random_state=0, solver='lbfgs', hidden_layer_sizes=[100, 10, 5], alpha=0.001)


def show_people_image_sample(people):
    fix, axes = plt.subplots(2, 5, figsize=(15, 8), subplot_kw={'xticks': (), 'yticks': ()})
    for target, image, ax in zip(people.target, people.images, axes.ravel()):
        ax.imshow(image)
        ax.set_title(people.target_names[target])


def print_photo_amout_per_people(people):
    counts = np.bincount(people.target)
    for i, (count, name) in enumerate(zip(counts, people.target_names)):
        print(f'{name:25} {count:3}', end=' ')
        if (i + 1) % 3 == 0:
            print()
    print()


def show_(tr, image_shape):
    fix, axes = plt.subplots(3, 5, figsize=(15, 12), subplot_kw={'xticks': (), 'yticks': ()})
    for i, (component, ax) in enumerate(zip(tr.components_, axes.ravel())):
        ax.imshow(component.reshape(image_shape), cmap='viridis')
        ax.set_title("{}. component".format((i + 1)))


def digits_t():
    digits = load_digits()
    # fig, axes = plt.subplots(2, 5, figsize=(10, 5), subplot_kw={'xticks': (), 'yticks': ()})
    # for ax, img in zip(axes.ravel(), digits.images):
    #     ax.imshow(img)

    # digits_pca = PCA(n_components=2).fit(digits.data).transform(digits.data)
    # show_digits(digits, digits_pca)

    tsne = TSNE(random_state=42)
    digits_tsne = tsne.fit_transform(digits.data)
    show_digits(digits, digits_tsne)


def show_digits(digits, transformator):
    colors = [
        "#476A2A", "#7851B8", "#BD3430", "#4A2D4E", "#875525", "#A83683", "#4E655E", "#853541", "#3A3120", "#535D8E"
    ]
    plt.figure(figsize=(10, 10))
    plt.xlim(transformator[:, 0].min(), transformator[:, 0].max() + 1)
    plt.ylim(transformator[:, 1].min(), transformator[:, 1].max() + 1)
    for i in range(transformator.shape[0]):
        plt.text(transformator[i, 0], transformator[i, 1], str(digits.target[i]), color=colors[digits.target[i]],
                 fontdict={'weight': 'bold', 'size': 9})
    plt.xlabel('C1')
    plt.ylabel('C2')


# pca_cancer()
# pca_faces()
# nmf_faces()
digits_t()
plt.show()
