import queens_problem
import random


# Okay, up here I will have the DFS core of the method: start with a random board
# Then, give each queen a fitness value based on the number of other queens it threatens
# Choose the maximum value
# Whenever we find an equal value to our current highest, we flip a coin on whether to replace it, for more randomness
# I also restart if we have been plateauing for too long
# Note that this algorithm has no way of knowing if the problem is insolvable, and in such a case, will keep trying
# forever
def solve_queen(size):
    number_of_moves = 0
    number_of_iterations = 0
    # these need to be variables outside the random restart, so that they don't get wiped when we restart
    should_random_restart = True
    while should_random_restart:
        should_random_restart = False
        columns = queens_problem.place_n_queens(size)

        number_of_moves += size  # since we have put down that many queens
        plateau_count = 0

        # central loop, where we search for the best move and do it
        while not should_random_restart:
            best_move = None
            best_fitness = float('-inf')

            # I start by going through each possibility and evaluating its fitness
            # If it is better, I replace my current best
            # If not, I ditch my current best
            for row in range(size):
                # I am not increasing iterations here, because I do so in the fitness function instead
                # Fitness measures number of conflicts, so we want to find what has the biggest fitness and fix it
                fitness, number_of_iterations = fitness_function(columns, row, number_of_iterations)
                if fitness > best_fitness or (fitness == best_fitness and random.random() > 0.5):
                    # if it's a bigger problem, or it is the same level problem, in which case we flip a coin
                    # then we record the new value
                    best_fitness = fitness
                    best_move = row

            # If the greatest number of conflicts is 0, then there are no conflicts, and we have a solution
            if best_fitness == 0:
                # print("I did it! Here is my solution")
                # print(columns)
                # queens_problem.display(columns)
                return number_of_iterations, number_of_moves
            else:
                # Since we have a problem to fix, we take the problematic column, find the best move, and do it
                columns[best_move], min_value, number_of_iterations = choose_best_move(columns, best_move,
                                                                                       number_of_iterations)
                number_of_moves += 2
                if min_value == best_fitness:  # if the number of conflicts we have after the move equals the
                    # number we had before the move
                    plateau_count += 1  # because we didn't actually improve the board
                    if plateau_count >= size:
                        # We have been plateauing for too long. It's time for a random restart
                        should_random_restart = True
                        number_of_moves += size  # because we are wiping off the board
                        # I'm not quite sure what this threshold should be
                        # But it felt appropriate to allow more wandering around when the playing field is bigger


# choose best move
def choose_best_move(columns, row, num_iterations):
    # we need to figure out what the best way to move it is

    horizontal_conflicts = {}
    up_diagonal_conflicts = {}
    down_diagonal_conflicts = {}

    for row_index, column in enumerate(columns):
        if row_index != row:  # if this is the same row, we don't double-count it
            horizontal_conflicts[column] = horizontal_conflicts.get(column, 0) + 1
            # increase its value by 1, adding it if it wasn't already there
            up_diagonal_conflicts[row_index + column] = up_diagonal_conflicts.get(row_index + column, 0) + 1
            down_diagonal_conflicts[row_index - column] = down_diagonal_conflicts.get(row_index - column, 0) + 1

    # now we should have a dictionary containing the number of conflicts in each column and diagonal, excluding the
    # element that we are looking for
    # So, for column, we just check for others with the same column
    # For the up_diagonal, we are searching for others with the same row + column
    # For the down_diagonal, we are searching for others with the same row - column
    min_column = None
    min_value = float('inf')
    for column in range(len(columns)):
        value = horizontal_conflicts.get(column, 0) + up_diagonal_conflicts.get(row + column, 0) + \
                down_diagonal_conflicts.get(row - column, 0)
        if value < min_value or value == min_value and random.random() > 0.5:
            min_value = value
            min_column = column

    num_iterations += 2 * len(columns)  # because we loop twice through the rows
    return min_column, min_value, num_iterations


# This is the fitness function I will be using
# It determines how many other queens the queen in this row is in conflict with
# It also updates the num_iterations accordingly
def fitness_function(columns, row, num_iterations):
    # there are no vertical conflicts by the definition of the data structure
    # to check horizontal conflicts, we check how many have the column's row

    num_conflicts = 0

    # check column
    num_conflicts += sum(1 for column in columns if column == columns[row]) - 1
    # subtract 1, because we want 0 conflicts if the only location of that number is

    # For checking the diagonal, I have discovered that adding the column number to the row number makes those in the
    # same upward diagonal equivalent.
    # While subtracting the column number from the row number makes those in the same downward diagonal equivalent.
    # Upward diagonal
    num_conflicts += sum(1 for this_row, col in enumerate(columns) if this_row + col == row + columns[row]) - 1
    # Downward diagonal
    num_conflicts += sum(1 for this_row, col in enumerate(columns) if this_row - col == row - columns[row]) - 1
    num_iterations += 3 * len(columns)
    return num_conflicts, num_iterations


'''
Here, you can find my (commented-out) tests for my fitness function.
def unit_test_fitness(board, row, expected):
    print("Testing board " + str(board) + " at row " + str(row))
    result = alt_fitness_function(board, row, 0)[0]
    if expected == result:
        print("Test success!")
    else:
        print("Test failed: expected " + str(expected) + " but received " + str(result))


# Okay, now let's test the fitness function
# Let's start with simple 4-length
# [0, 0, 0, 0] with any row should have a fitness of 3, since that is how many conflicts each one has
unit_test_fitness([0, 0, 0, 0], 0, 3)
unit_test_fitness([0, 0, 0, 0], 0, 3)
# The simple diagonal cases should also be 3
unit_test_fitness([0, 1, 2, 3], 0, 3)
unit_test_fitness([3, 2, 1, 0], 1, 3)
# My corner case had 4 conflicts, with each location having 2
unit_test_fitness([1, 0, 3, 2], 3, 2)
unit_test_fitness([1, 0, 3, 2], 2, 2)
# Let's test the completed problem
unit_test_fitness([2, 0, 3, 1], 0, 0)
unit_test_fitness([2, 0, 3, 1], 1, 0)
# Let's test an angular case, which should be 2 from the first 2, 3 from the middle, and 1 for the edge
unit_test_fitness([0, 1, 2, 2], 0, 2)
unit_test_fitness([0, 1, 2, 2], 1, 2)
unit_test_fitness([0, 1, 2, 2], 2, 3)
unit_test_fitness([0, 1, 2, 2], 3, 1)
# And an almost-complete with a score of 3, where 0, 1, and 2 and get 1, and 3 gets 3
unit_test_fitness([2, 0, 3, 2], 0, 1)
unit_test_fitness([2, 0, 3, 2], 1, 1)
unit_test_fitness([2, 0, 3, 2], 2, 1)
unit_test_fitness([2, 0, 3, 2], 3, 3)
# And a really almost-complete with a score of 1 from 2 and 3 and 0 from 1 and 2
unit_test_fitness([2, 0, 3, 3], 0, 0)
unit_test_fitness([2, 0, 3, 3], 1, 0)
unit_test_fitness([2, 0, 3, 3], 2, 1)
unit_test_fitness([2, 0, 3, 3], 3, 1)
# '''

'''
This has the unit tests for my function to find the best column to put a queen in when I have already decided to move it
def unit_test_choose_best(board, row, expected):
    print("Testing board " + str(board) + " at row " + str(row))
    result = choose_best_move(board, row, 0)[0]
    if result == expected or result in expected:
        print("Test success!")
    else:
        print("Test failed: expected " + str(expected) + " but received " + str(result))


# Okay, let's test 3 of the cases from before
# For flat on the top, no matter which we choose, we want to bring it to the bottom
unit_test_choose_best([0, 0, 0, 0], 0, (1, 2, 3))
unit_test_choose_best([0, 0, 0, 0], 1, (3, 'tuple'))
unit_test_choose_best([0, 0, 0, 0], 2, (3, 'tuple'))
unit_test_choose_best([0, 0, 0, 0], 3, (1, 2, 3))
# for down diagonal
# for 0, 1 and 3 have 1 conflict, while 2 has 2
unit_test_choose_best([0, 1, 2, 3], 0, (1, 3))
unit_test_choose_best([0, 1, 2, 3], 1, (0, 2))
unit_test_choose_best([0, 1, 2, 3], 2, (1, 3))
unit_test_choose_best([0, 1, 2, 3], 3, (0, 2))
# My corner case had 4 conflicts, with each location having 2
unit_test_choose_best([1, 0, 3, 2], 0, (0, 2, 3))
unit_test_choose_best([1, 0, 3, 2], 1, (1, 3))
unit_test_choose_best([1, 0, 3, 2], 2, (0, 2))
unit_test_choose_best([1, 0, 3, 2], 3, (0, 1, 3))
# Finally, let's test a victory scenario
unit_test_choose_best([2, 0, 3, 3], 3, (1, 'tuple'))
# '''
