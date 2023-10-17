import queens_problem


def solve_queen(size):
    columns = []

    number_of_moves = 0
    number_of_iterations = 0
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        # place queen in next row
        # print(columns)
        # print("I have ", row, " number of queens put down")
        # display()
        # print(number_of_moves)
        while column < size:
            number_of_iterations += 1
            number_of_moves += 1  # we placed a queen, so we count it
            # it's possible that we immediately remove it, but if so, we still placed it
            if queens_problem.next_row_is_safe(columns, column, size):
                queens_problem.place_in_next_row(columns, column)
                row += 1
                column = 0
                break
            else:
                column += 1
                number_of_moves += 1  # we removed the queen as soon as we placed it
        # if I could not find an open column or if board is full
        if column == size or row == size:
            number_of_iterations += 1
            # I'm not sure why this counts as an iteration, but I didn't add a queen, so I'm not counting it as a move
            # if board is full, we have a solution
            if row == size:
                # I have these commented out, so that they don't spam me when doing it 100 times
                # print("I did it! Here is my solution")
                # queens_problem.display(columns)
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = queens_problem.remove_in_current_row(columns)
            number_of_moves += 1  # We remove the queen, so we count it as a move
            if prev_column == -1:  # I backtracked past column 1
                print("There are no solutions")
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column
