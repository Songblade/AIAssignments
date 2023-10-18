import dfs_with_backtracking
import british_museum
import hill_climbing
import time


def run_and_display_queens_algorithm(algorithm, size, should_display=True):
    if should_display:
        print()
    start_time = time.time()
    num_iterations, num_moves = algorithm(size)
    elapsed_time = time.time() - start_time
    if num_moves == 0:
        num_moves = "unknown"
    if should_display:
        print("Took " + str(num_iterations) + " iterations, " + str(num_moves) + " moves, and " + str(elapsed_time) +
              " seconds")
    else:
        return num_iterations, num_moves, elapsed_time


def collect_data_for_queens_algorithm(algorithm, trying_hard):
    elapsed_time = 0
    num_queens = 10
    while not taking_too_long(elapsed_time, trying_hard):
        start_time = time.time()
        total_iterations, total_moves, total_time = 0, 0, 0
        for i in range(100):
            results = run_and_display_queens_algorithm(algorithm, num_queens, False)
            total_iterations += results[0]
            total_moves += results[1]
            total_time += results[2]
        average_iterations = total_iterations / 100
        average_moves = total_moves / 100
        average_time = total_time / 100
        print("With " + str(num_queens) + ", we have " + str(average_iterations) + " iterations, " +
              str(average_moves) + " moves, and " + str(average_time) + " seconds")
        elapsed_time = time.time() - start_time
        num_queens += 1


# we are taking too long if a single iteration of 100 took more than a second each
# But for my best one, I will probably need to allow more time than that to reach 40, so I'm going to wait 5 seconds
# (I might increase that time later)
def taking_too_long(elapsed_time, trying_hard):
    if (trying_hard and elapsed_time > 500) or (not trying_hard and elapsed_time > 100):
        return True
    return False


# run_and_display_queens_algorithm(dfs_with_backtracking.solve_queen, 4)
# run_and_display_queens_algorithm(hill_climbing.solve_queen, 40)
# collect_data_for_queens_algorithm(dfs_with_backtracking.solve_queen, False)
# collect_data_for_queens_algorithm(british_museum.solve_queen, False)
collect_data_for_queens_algorithm(hill_climbing.solve_queen, False)
