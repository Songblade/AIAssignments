import queens_problem


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


def solve_queen(size, columns=None):
    if columns is None:
        columns = []

    number_of_moves = 0  # where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        # place queen in next row
        # print(columns)
        # print("I have ", row, " number of queens put down")
        # display()
        print(number_of_moves)
        while column < size:
            number_of_iterations += 1
            if next_row_is_safe(columns, column, size):
                place_in_next_row(columns, column)
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if column == size or row == size:
            number_of_iterations += 1
            # if board is full, we have a solution
            if row == size:
                print("I did it! Here is my solution")
                queens_problem.display(columns)
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row(columns)
            if prev_column == -1:  # I backtracked past column 1
                print("There are no solutions")
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column
