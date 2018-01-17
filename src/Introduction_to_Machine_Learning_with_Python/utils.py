from matplotlib import pyplot as plt


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
