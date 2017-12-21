import numpy as np
import matplotlib.pyplot as plt


names = np.array(['Bob', 'Joe', 'Will', 'JBob', 'Will', 'Joe', 'Joe'])

# data = np.random.randn(7, 4)
# plt.plot(data)
print(np.array(list(map(lambda x: x[0], names))))
print(names[np.array(list(map(lambda x: x[0], names))) == 'J'])
# print(names[names == 'Bob'])
# print(data)
# print(data[[0, 2, 6]])
# print(np.ones((2, 2)))
#
# m = np.arange(16).reshape((2, 2, 4))
# print(m.strides)
#
# print()
# print(m)
# print(m.transpose((1, 0, 2)))
#
# print(np.dot(m.T, m))
# plt.show(True)