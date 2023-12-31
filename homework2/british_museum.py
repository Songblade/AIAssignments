import queens_problem


def board_is_safe(columns):
    size = len(columns)
    for index, column in enumerate(columns):
        if not queens_problem.next_row_is_safe(columns[:index], column, size):
            return False
    return True


def solve_queen(size):
    num_iterations = 0
    num_moves = 0
    while True:
        num_iterations += 1
        num_moves += size  # since we are adding size more, and dumping the board doesn't count
        # so we are removing the previous 16 and adding the next one
        columns = queens_problem.place_n_queens(size)
        if board_is_safe(columns):
            # I have these commented out, so that they don't spam me when I do it 100 times
            # print("I did it! Here is my solution")
            # queens_problem.display(columns)
            return num_iterations, num_moves
