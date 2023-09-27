import random


size = 8


# columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
# If columns isn't specified, we start over
def place_n_queens(side_length, columns=None):
    if columns is None:
        columns = []
    # I don't know why, but Python thinks that having immutable default parameters is bad style

    row = 0
    while row < side_length:
        column = random.randrange(0, side_length)
        columns.append(column)
        row += 1
    return columns


def display(columns):
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()


display(place_n_queens(size))
