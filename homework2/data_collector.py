import dfs_with_backtracking
import british_museum
import time


def run_and_display_queens_algorithm(algorithm, size):
    print()
    start_time = time.time()
    num_iterations, num_moves = algorithm(size)
    elapsed_time = time.time() - start_time
    if num_moves == 0:
        num_moves = "unknown"
    print("Took " + str(num_iterations) + " iterations, " + str(num_moves) + " moves, and " + str(elapsed_time) +
          " seconds")


run_and_display_queens_algorithm(dfs_with_backtracking.solve_queen, 8)
run_and_display_queens_algorithm(british_museum.solve_queen, 8)

run_and_display_queens_algorithm(dfs_with_backtracking.solve_queen, 4)
