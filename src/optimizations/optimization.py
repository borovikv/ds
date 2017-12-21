import math
import random
import time

import pandas as pd

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# Место назначения – аэропорт Ла Гардиа в Нью-Йорке
DESTINATION = 'LGA'

flights = pd.read_csv('schedule.txt',
                      names=['origin', 'dest', 'depart', 'arrive', 'price'],
                      index_col=['origin', 'dest']).sort_index()


def schedulecost(sol):
    df = schedule(sol)
    # Полная цена равна сумме цен на билет туда и обратно
    totalprice = df.out_price.sum() + df.ret_price.sum()

    # Находим самый поздний прилет и самый ранний вылет
    latestarrival = df.arrive_m.max()
    earliestdep = df.departure_m.min()

    # Все должны ждать в аэропорту прибытия последнего участника группы.
    # Обратно все прибывают одновременно и должны ждать свои рейсы.
    totalwait = (-(df.arrive_m - latestarrival) + (df.departure_m - earliestdep)).sum()
    # Для этого решения требуется оплачивать дополнительный день аренды?
    # Если да, это обойдется в лишние $50!
    if latestarrival > earliestdep:
        totalprice += 50

    return totalprice + totalwait


# solution 1
def randomoptimize(domain, costf):
    best = 999999999
    solution = None
    for i in range(10000):
        # Выбрать случайное решение
        r = random_solution(domain)
        # Вычислить его стоимость
        cost = costf(r)
        # Сравнить со стоимостью наилучшего найденного к этому моменту решения
        if cost < best:
            best = cost
            solution = r
    return solution


def random_solution(domain):
    return [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]


# solution 2
def hillclimb(domain, costf):
    # Выбрать случайное решение
    solution = random_solution(domain)
    # Главный цикл
    while True:
        # Создать список соседних решений
        neighbors = []
        for i in range(len(domain)):
            # Отходим на один шаг в каждом направлении
            if solution[i] > domain[i][0]:
                neighbors.append(solution[0:i] + [solution[i] + 1] + solution[i + 1:])
            if solution[i] < domain[i][1]:
                neighbors.append(solution[0:i] + [solution[i] - 1] + solution[i + 1:])

        # Ищем наилучшее из соседних решений
        current = costf(solution)
        best = current
        for neighbor in neighbors:
            cost = costf(neighbor)
            if cost < best:
                best = cost
                solution = neighbor
        # Если улучшения нет, мы достигли дна
        if best == current:
            break
    return solution


# solution 3
def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
    # Инициализировать переменные случайным образом
    vec = random_solution(domain)
    while T > 0.1:
        # Выбрать один из индексов
        i = random.randint(0, len(domain) - 1)
        # Выбрать направление изменения
        dir = random.randint(-step, step)
        # Создать новый список, в котором одно значение изменено
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        # Вычислить текущую и новую стоимость
        ea = costf(vec)
        eb = costf(vecb)
        # Вычислить вероятность, которая уменьшается с уменьшением T
        p = pow(math.e, (-eb - ea) / T)
        # Новое решение лучше? Если нет, метнем кости
        if eb < ea or random.random() < p:
            vec = vecb
        # Уменьшить температуру
        T = T * cool
    return vec


def schedule(r):
    flying_peoples = people[:int(len(r) / 2)]
    df = pd.DataFrame(
        [person_schedule(name, origin, r[i], r[i + 1]) for i, (name, origin) in enumerate(flying_peoples)]
    )
    df['arrive_m'] = df.out_arrive.apply(getminutes)
    df['departure_m'] = df.ret_depart.apply(getminutes)
    return df


def person_schedule(name, origin, out, dep):
    return dict(
        name=name,
        origin=origin,
        **flight_info(origin, DESTINATION, out, 'out'),
        **flight_info(DESTINATION, origin, dep, 'ret')
    )


def flight_info(origin, destination, flight_number, prefix: str):
    flight = flights.loc[(origin, destination)].iloc[int(flight_number)]
    return {f'{prefix}_{key}': value for key, value in flight.to_dict().items()}


def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x.tm_hour * 60 + x.tm_min


domain = [(0, 8)] * (len(people) * 2)
import time
for i in range(10):
    for f in [randomoptimize, hillclimb, annealingoptimize]:
        start = time.time()
        sol = f(domain, schedulecost)
        end = time.time()
        print(schedulecost(sol))
        print(f.__name__, end - start)

