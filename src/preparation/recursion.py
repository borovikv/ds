def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


def is_blocked(matrix, row, col):
    return matrix[row][col] == 1 or len(matrix) == row or len(matrix[0]) == col


def block(matrix, row, col):
    matrix[row][col] = 1


def print_m(m):
    print('-' * 7)
    for row in m:
        print(row)
    print('-' * 7)


def find_path(matrix, row=0, col=0, path=()):
    rows = len(matrix)
    cols = len(matrix[0])
    if row == rows - 1 and col == cols - 2:
        return path + ((row, col + 1),)
    if col == cols - 1 and row == rows - 2:
        return path + ((row + 1, col),)
    if is_blocked(matrix, row, col + 1) and is_blocked(matrix, row + 1, col):
        block(matrix, row, col)
        return find_path(matrix, max(0, row - 1), max(0, col - 1), path[:-1])
    if not is_blocked(matrix, row, col + 1):
        return find_path(matrix, row, col + 1, path + ((row, col + 1),))
    else:
        return find_path(matrix, row + 1, col, path + ((row + 1, col),))


def get_path(maze, row, col, path=None, cache=None):
    if cache is None:
        cache = {}
    if col < 0 or row < 0 or is_blocked(maze, row, col):
        return False
    point = (row, col)
    if point in cache:
        print('k')
        return cache[point]

    is_at_origin = row == 0 and col == 0
    success = False
    if is_at_origin or get_path(maze, row, col - 1, path, cache) or get_path(maze, row - 1, col, path, cache):
        path.append(point)
        success = True
    cache[point] = success
    return success


matrix = [
    [0, 0, 1],
    [0, 1, 0],
    [0, 0, 0],
]

print(find_path(matrix))
path = []
c = {}
print(get_path(matrix, row=len(matrix) - 1, col=len(matrix[0]) - 1, path=path, cache=c))
print(c)
print(path)


def make_change(amount, coins, index):
    if index >= len(coins) - 1:
        return 1
    coin = coins[index]
    ways = 0
    for i in range(0, amount + 1, coin):
        ways += make_change(amount - i, coins, index + 1)
    return ways


print(make_change(10, [25, 10, 5, 1], 0))

GRID_SIZE = 8


def place_queens(row, columns: list, results: list):
    if row == GRID_SIZE:
        results.append(list(columns))
    else:
        for col in range(GRID_SIZE):
            if check_valid(columns, row, col):
                columns[row] = col
                place_queens(row + 1, columns, results)


def check_valid(columns, row, col):
    for r in range(row):
        c = columns[r]
        if c == col:
            return False
        # check diagonal
        col_distance = abs(c - col)
        row_distance = row - r
        if col_distance == row_distance:
            return False
    return True


columns = [None] * GRID_SIZE
results = []
place_queens(0, columns, results)
print(results)


def create_stack_2(boxes, bottom, offset, stack):
    if offset >= len(boxes):
        return 0

    new_bottom = boxes[offset]
    height_with_bottom = 0
    if bottom is None or new_bottom < bottom:
        if stack[offset] == 0:
            stack[offset] = create_stack_2(boxes, new_bottom, offset + 1, stack) + new_bottom.height
        height_with_bottom = stack[offset]
    height_without_bottom = create_stack_2(boxes, bottom, offset + 1, stack)
    return max(height_with_bottom, height_without_bottom)


def create_stack(boxes):
    boxes = sorted(boxes)
    return create_stack_2(boxes, None, 0, [None] * len(boxes))
