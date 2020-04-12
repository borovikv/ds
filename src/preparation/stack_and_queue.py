from collections import deque


def example():
    stack = [1, 2, 3, 4]
    queue = deque([1, 2, 3, 4])
    for i in range(4):
        print(f'{i}: stack {stack.pop()} | queue {queue.popleft()}')


class Stack:
    def __init__(self):
        self.stack_indexes = dict(zip('abc', [-3, -2, -1]))
        self.initial_stack_indexes = dict(zip('abc', [-3, -2, -1]))
        self.stack = [None] * len(self.stack_indexes)

    def pop(self, stack):
        stack_index = self.stack_indexes[stack]
        if stack_index == self.initial_stack_indexes[stack]:
            return None
        result = self.stack[stack_index]
        stack_index -= len(self.stack_indexes)
        self.stack_indexes[stack] = stack_index
        return result

    def add(self, stack, value):
        stack_index = self.stack_indexes[stack]
        stack_index += len(self.stack_indexes)
        if len(self.stack) <= stack_index:
            self.stack += [None] * len(self.stack_indexes)
        self.stack[stack_index] = value
        self.stack_indexes[stack] = stack_index


class SetOfStacks:
    def __init__(self):
        self.stacks = [[]]
        self.max_length = 3

    def push(self, value):
        if len(self.stacks[-1]) == self.max_length:
            self.stacks.append([])
        self.stacks[-1].append(value)

    def pop(self, index=-1):
        value = self.stacks[index].pop()
        if len(self.stacks[index]) == 0:
            del self.stacks[index]
        return value

    def __repr__(self):
        return str(self.stacks)


class SortedStack:
    def __init__(self):
        self.stack = []
        self._stack = []

    def push(self, value):
        if len(self.stack) == 0 or self.stack[-1] >= value:
            self.stack.append(value)
            self.stack += list(reversed(self._stack))
            self._stack = []
        else:
            e = self.stack.pop()
            self._stack.append(e)
            self.push(value)

    def __repr__(self):
        return str(self.stack)


# import random
from collections import deque
if __name__ == '__main__':
    pass
    # s = SortedStack()
    # for i in range(10):
    #     value = random.randint(20, 30)
    #     s.push(value)
    #     print(value, s)
    # s = SetOfStacks()
    # for i in range(10):
    #     s.push(i)
    # print(s)
    # print(s.pop(0))
    # print(s)
    # print(s.pop(0))
    # print(s)
    # print(s.pop(0))
    # print(s)
    # a = [list('abc')]
    # print(a)
    # inner = a[0]
    # for i in range(10000):
    #     a.append(list('xyz'))
    # inner[0] = 'A'
    # print(a[0])

    # example()
    # print(float('-inf'))
    # a = Stack()
    # a.add('a', 1)
    # a.add('a', 2)
    # a.add('a', 3)
    # a.add('b', 'z')
    # a.add('b', 'x')
    # a.add('b', 'y')
    # a.add('c', 10)
    # a.add('c', 20)
    # a.add('c', 30)
    # print(a.pop('a'))
    # print(a.pop('b'))
    # print(a.pop('c'))
    # print(a.pop('a'))
    # print(a.pop('b'))
    # print(a.pop('c'))
    # print(a.pop('a'))
    # print(a.pop('b'))
    # print(a.pop('c'))
    # print(a.pop('a'))
    # a.add('a', 100)
    # print(a.pop('b'))
    # print(a.pop('c'))
    # print(a.pop('a'))
    # print(a.pop('b'))
    # print(a.pop('c'))
    # print(a.pop('a'))
    # print(a.pop('b'))
    # print(a.pop('c'))
