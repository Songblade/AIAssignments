import random


# columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
# If columns isn't specified, we start over
def place_n_queens(side_length):
    columns = []
    # I don't know why, but Python thinks that having immutable default parameters is bad style

    row = 0
    while row < side_length:
        column = random.randrange(0, side_length)
        columns.append(column)
        row += 1
    return columns


def place_in_next_row(columns, column):
    columns.append(column)


def remove_in_current_row(columns):
    if len(columns) > 0:
        return columns.pop()
    return -1


def next_row_is_safe(columns, column, size):
    row = len(columns)
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False

    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False

    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if (size - queen_column) - queen_row == (size - column) - row:
            return False
    return True


def display(columns):
    size = len(columns)
    for row in range(size):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

# TODO: Update DFS to count number of moves
# TODO: Finish British Museum
# TODO: Do Heuristic Repair/Stochastic Search
# TODO: Do Forward Checking
