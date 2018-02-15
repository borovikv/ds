import ssl

import mglearn
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import fetch_lfw_people


def score(method, X_train, X_test, y_train, y_test, plot=False, **kwargs):
    clf = method(**kwargs)
    clf.fit(X_train, y_train)
    print(f'{method.__name__} with {kwargs}')
    print(f"Правильность на обучающем наборе: {clf.score(X_train, y_train):.3f}")
    print(f"Правильность на тестовом наборе: {clf.score(X_test, y_test):.3f}")
    print('-' * 100)
    if plot:
        prediction = clf.predict(X_test)
        plt.plot(X_test, prediction, '*')
    return clf


def scale_std(X_train, X_test):
    mean_on_train = X_train.mean(axis=0)
    std_on_train = X_train.std(axis=0)
    X_train_scaled = (X_train - mean_on_train) / std_on_train
    X_test_scaled = (X_test - mean_on_train) / std_on_train
    return X_train_scaled, X_test_scaled


def curry(X_train, X_test, y_train, y_test):
    def function(method, **kwargs):
        return score(method, X_train, X_test, y_train, y_test, plot=False, **kwargs)

    return function


def scale_range(X_train, X_test):
    # вычисляем минимальное значение для каждого признака обучающего набора
    min_on_training = X_train.min(axis=0)
    # вычисляем ширину диапазона для каждого признака (max - min) обучающего набора
    range_on_training = (X_train - min_on_training).max(axis=0)
    # вычитаем минимальное значение и затем делим на ширину диапазона
    # min=0 и max=1 для каждого признака
    X_train_scaled = (X_train - min_on_training) / range_on_training
    X_test_scaled = (X_test - min_on_training) / range_on_training
    print("Минимальное значение для каждого признака\n{}".format(X_train_scaled.min(axis=0)))
    print("Максимальное значение для каждого признака\n {}".format(X_train_scaled.max(axis=0)))
    return X_train_scaled, X_test_scaled


def draw_mlp_map(mlp, feature_names):
    plt.figure(figsize=(20, 5))
    plt.imshow(mlp.coefs_[0], interpolation='none', cmap='viridis')
    plt.yticks(range(30), feature_names)
    plt.xlabel("Столбцы матрицы весов")
    plt.ylabel("Входные характеристики")
    plt.colorbar()


def histograms_by_features(dataset):
    fig, axes = plt.subplots(15, 2, figsize=(10, 20))
    targets = [dataset.data[dataset.target == t] for t in np.unique(dataset.target)]
    ax = axes.ravel()
    for i in range(len(dataset.feature_names)):
        _, bins = np.histogram(dataset.data[:, i], bins=50)
        for j, data_group in enumerate(targets):
            ax[i].hist(data_group[:, i], bins=bins, color=mglearn.cm3(j * 2), alpha=.5)
        ax[i].set_title(dataset.feature_names[i])
        ax[i].set_yticks(())
    ax[0].set_xlabel("Feature value")
    ax[0].set_ylabel("Frequency")
    ax[0].legend(dataset.target_names, loc="best")
    fig.tight_layout()


def get_people():
    ssl._create_default_https_context = ssl._create_unverified_context
    people = fetch_lfw_people(min_faces_per_person=20, resize=0.7)
    # image_shape = people.images[0].shape
    # print(people.images.shape)
    # print(image_shape)
    # print_photo_amout_per_people(people)
    # show_people_image_sample(people)
    mask = np.zeros(people.target.shape, dtype=np.bool)
    for target in np.unique(people.target):
        mask[np.where(people.target == target)[0][:50]] = 1
    y_people = people.target[mask]
    X_people = people.data[mask]
    X_people = X_people / 255.
    # print(len(X_people[1]))
    # print(len(X_people))
    return people, X_people, y_people
