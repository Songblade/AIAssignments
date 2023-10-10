import queens_problem


def board_is_safe(columns):
    size = len(columns)
    for index, column in enumerate(columns):
        if not queens_problem.next_row_is_safe(columns[:index], column, size):
            return False
    return True


def solve_queen(size):
    num_iterations = 0
    while True:
        num_iterations += 1
        columns = queens_problem.place_n_queens(size)
        if board_is_safe(columns):
            print("I did it! Here is my solution")
            queens_problem.display(columns)
            return num_iterations, 0
