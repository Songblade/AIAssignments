import math
import queens_problem
import random


# Okay, up here I will have the DFS core of the method: start with a random board
# Then, figure out the branching factor, all possible moves, and give each a fitness value
# Choose the minimum value
# Whenever we find an equal value to our current lowest, we flip a coin on whether to replace it, to add more randomness
# I'm going to want to add a random restart or the like, but right now, let's just try the base model
def solve_queen(size):
    number_of_moves = 0
    number_of_iterations = 0
    # these need to be variables outside the random restart, so that they don't get wiped when we restart
    should_random_restart = True
    while should_random_restart:
        should_random_restart = False
        columns = queens_problem.place_n_queens(size)

        number_of_moves += size  # since we have put down that many queens
        number_of_iterations = 0
        best_fitness = float('inf')

        # central loop, where we search for the best move and do it
        while best_fitness > 0 and not should_random_restart:
            local_best_move = None
            local_best_fitness = float('inf')

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
                number_of_iterations += 1  # perhaps I should increase it by 2, since I check two moves in one iteration
                # I only increase it here, because it is the center-most loop, and includes all the others
                # Though if the fitness function counts, then I should be including it there instead
                if columns[row] < size - 1:
                    # Only try the move + 1 if that doesn't get us out of bounds
                    columns[row] += 1
                    number_of_moves += 2
                    fitness = fitness_function(columns)
                    if fitness < local_best_fitness or (fitness == local_best_fitness and random.random() > 0.5):
                        # if it's an improvement, or it makes no change, in which case we flip a coin
                        # then we record the new value
                        local_best_fitness = fitness
                        local_best_move = (row, columns[row])
                    columns[row] -= 1  # so no lasting effects
                if columns[row] > 0:
                    # Only try the move - 1 if that doesn't get us out of bounds
                    columns[row] -= 1
                    number_of_moves += 2
                    fitness = fitness_function(columns)
                    if fitness < local_best_fitness or (fitness == local_best_fitness and random.random() > 0.5):
                        # if it's an improvement, or it makes no change, in which case we flip a coin
                        # then we record the new value
                        local_best_fitness = fitness
                        local_best_move = (row, columns[row])
                    columns[row] += 1  # so no lasting effects

            # Now we look at the best move and implement it
            # In the future, I could probably do stuff here to check if I need a random restart
            # But right now, I'm not doing that
            # I'll do that if I need a performance boost
            if local_best_fitness <= best_fitness:
                best_fitness = local_best_fitness
                best_move = local_best_move
                columns[best_move[0]] = best_move[1]
                number_of_moves += 1
            else:
                # in a case where the local best is actually worse than the previous best, we are at a local maximum
                # and should restart
                should_random_restart = True

        if not should_random_restart:
            # we get here if we reached a fitness level of 0 after the previous change
            # In which case we are done and ready to return
            # If we break out of the loop because of a random restart, we aren't ready to end just yet
            print("I did it! Here is my solution")
            queens_problem.display(columns)
            return number_of_iterations, number_of_moves




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
def fitness_function(columns):
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

    return num_conflicts


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
    return sum(math.comb(duplicates, 2) for duplicates in row_nums.values())


'''
def unit_test_fitness(board, expected):
    print("Testing board " + str(board))
    result = fitness_function(board)
    if expected == result:
        print("Test success!")
    else:
        print("Test failed: expected " + str(expected) + " but received " + str(result))



# Okay, now let's test the fitness function
# Let's start with simple 4-length
# [0, 0, 0, 0] should have a fitness of 6, since that is how many times they are blocking each other
unit_test_fitness([0, 0, 0, 0], 6)
# The simple diagonal cases should also be 6
unit_test_fitness([0, 1, 2, 3], 6)
unit_test_fitness([3, 2, 1, 0], 6)
# My corner case had 4 conflicts
unit_test_fitness([1, 0, 3, 2], 4)
# Let's test the completed problem
unit_test_fitness([2, 0, 3, 1], 0)
# Let's test an angular case, which should also be 4
unit_test_fitness([0, 1, 2, 2], 4)
# And an almost-complete with a score of 3
unit_test_fitness([2, 0, 3, 2], 3)
# And a really almost-complete with a score of 1
unit_test_fitness([2, 0, 3, 3], 1)
'''
