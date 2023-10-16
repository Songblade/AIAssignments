import queens_problem


def board_is_safe(columns):
    size = len(columns)
    for index, column in enumerate(columns):
        if not queens_problem.next_row_is_safe(columns[:index], column, size):
            return False
    return True


def solve_queen(size):
    num_iterations = 0
    num_moves = -size  # because I am adding size each time
    # But we don't need to remove the previous size queens on the first iteration when the board is clear.
    while True:
        num_iterations += 1
        num_moves += 2 * size  # since we are removing the previous size queens and adding size more
        # so we are removing the previous 16 and adding the next one
        columns = queens_problem.place_n_queens(size)
        if board_is_safe(columns):
            print("I did it! Here is my solution")
            queens_problem.display(columns)
            return num_iterations, num_moves
