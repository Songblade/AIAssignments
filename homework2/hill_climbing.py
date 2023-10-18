import math
import queens_problem
import random


# Okay, up here I will have the DFS core of the method: start with a random board
# Then, figure out the branching factor, all possible moves, and give each a fitness value
# Choose the minimum value
# Whenever we find an equal value to our current lowest, we flip a coin on whether to replace it, to add more randomness
# I also restart if I have reached a local minima or have been plateauing for too long
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

            # Question: How many branches do I want to look at?
            # Am I only moving queens one move?
            # If so, I will have a number of possibilities equal to 2n
            # If I am moving the queen every number of moves, I will have a number equal to n(n-1), which is n^2
            # I'm going to go with the smaller number of possibilities for now, but might change my mind later
            # So, how do I figure out all possible moves?
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

            # If the greatest number of conflicts is 0, we have a solution
            if best_fitness == 0:
                # print("I did it! Here is my solution")
                # print(columns)
                # print(board_is_done(columns))
                # queens_problem.display(columns)
                return number_of_iterations, number_of_moves
            else:
                # Since we have a problem to fix, we take the problematic column, find the best move, and do it
                columns[best_move], min_value, number_of_iterations = choose_best_move(columns, best_move,
                                                                                       number_of_iterations)
                number_of_moves += 2
                if min_value == best_fitness:  # if the number of conflicts we have after the move equals the
                    # number we had before the move
                    plateau_count += 1
                    if plateau_count >= size:
                        should_random_restart = True
                        number_of_moves += size  # because we are wiping off the board
                        # I'm not quite sure what this threshold should be
                        # But it felt appropriate to allow more wandering around when the playing field is bigger

            '''
            I got rid of this stuff because I think it's messing me up
            # Now we look at the best move and implement it
            # and also check if we need to restart
            if local_best_fitness == best_fitness:
                # we could be plateauing
                # so, let's see if we can get ourselves out of this rut, but if not, restart
                plateau_count += 1
            elif local_best_fitness < best_fitness:
                plateau_count = 0

            if local_best_fitness <= best_fitness:
                best_fitness = local_best_fitness
                best_move = local_best_move
                columns[best_move], number_of_iterations = choose_best_move(columns, best_move, number_of_iterations)
                number_of_moves += 2
            else:
                # in a case where the local best is actually worse than the previous best, we are at a local maximum
                # and should restart
                should_random_restart = True
            
            if plateau_count >= size:
                should_random_restart = True
                # I'm not quite sure what this threshold should be
                # But it felt appropriate to allow more wandering around when the playing field is bigger
                # And I couldn't get better results by messing around a little

        if not should_random_restart:
            # we get here if we reached a fitness level of 0 after the previous change
            # In which case we are done and ready to return
            # If we break out of the loop because of a random restart, we aren't ready to end just yet
            # print("I did it! Here is my solution")
            # queens_problem.display(columns)
            return number_of_iterations, number_of_moves
        else:
            number_of_moves += size  # because we are throwing them off the board
            
            '''


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

    num_iterations += 2 * len(columns)
    return min_column, min_value, num_iterations


'''
So, how do I figure out what the best move is?
I could go through every possible column and check its fitness, but that's going to be n^2
Is there a better way?
I can't really think of anything
But there has to be something better, or else I'm going to be taking forever
Hmm. Maybe, first I figure out how many conflicts there are with each possible number of columns
Then, we can go through each column and check if it works
If I'm correct (and I think I am, since it's how I generated conflicts before), this should only be O(n), much better
I just need to make sure not to double-count
Hold on. How do I add the diagonals to make sure everything is right?
I need to make sure that whatever diagonal 0 is in...
Hold on. I can't do that, because I don't know what diagonal everyone will be in
Instead, what I have to do is hold a separate index of each diagonal
Hold on. I do know what diagonal it will be. I need to figure out which diagonal our row will be in
So, how do we know if a given space is in another row's diagonal?
Let's say we need to know which diagonal of x row 2 will be in
Okay. Let's draw it out.
Whatever. Maybe I could, but it doesn't change the number of iterations, and it's not worth figuring out
'''

'''
The best way to randomly restart is, I think, to put everything in a loop. When we decide to randomly restart, we end
our current loop to get a new iteration on the greater loop.

The only things I should want from the previous loop are the counts of moves and iterations. Everything else - the 
columns, the best move, the best fitness - restart.
'''


# I'm not really sure what I'm doing for the stochastic method, as things don't seem very clear. Now I wish I paid
# attention during the previous class. Whatever, I'll pay attention on Monday, when people will hopefully ask questions
# But either way, I definitely need a fitness function, where I determine how good any given solution is
# So, let's start by writing that
# All I need to do is determine the number of conflicts in the set
# So, the smallest number is the best, and we seek a minimum value
def board_is_done(columns):
    # there are no vertical conflicts by the definition of the data structure
    # to check horizontal conflicts, we start by checking if there are any duplicate rows
    # The number of distinct rows is, let's see
    # If we have 6 distinct rows, that means that there were 2 more rows that had duplicates
    # Each of those is a conflict with 1 regular row, which means that the difference is num-conflicts
    # Only, that's not really true, because if there are multiple in the same row, it's a much bigger conflict
    # But I think I will ignore those. I don't think it really makes a difference for how bad it is

    num_conflicts = 0

    # check column
    num_conflicts += find_num_conflicts(columns)
    # the difference between the number of columns and the number of distinct columns

    # For checking the diagonal, I have discovered that adding the column number to the row number makes those in the
    # same upward diagonal equivalent.
    # While subtracting the column number from the row number makes those in the same downward diagonal equivalent.
    # Upward diagonal
    num_conflicts += find_num_conflicts(row + col for row, col in enumerate(columns))
    # Downward diagonal
    num_conflicts += find_num_conflicts(row - col for row, col in enumerate(columns))

    return num_conflicts == 0


# '''


# This is the real fitness function I will be using
# I forgot that the professor had mentioned something like it in class, that the fitness is how many conflicts a place
# currently has, not how much it will have.
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


def find_num_conflicts(columns):
    # This gets us the number of rows that use each column
    row_nums = {}
    for column in columns:
        if column in row_nums:
            row_nums[column] += 1
        else:
            row_nums[column] = 1

    # Now we need to go through each column and figure out how many conflicts it has
    # This is basically asking for the number of pairs you can make in a set of this size
    # This is l nCr 2, where nCr
    # They have that built in
    # I initially worried that that would take too long, but it ran instantaneously with a billion nCr 2, so...
    # return sum(duplicates - 1 for duplicates in row_nums.values())
    return sum(math.comb(duplicates, 2) for duplicates in row_nums.values())


'''
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
