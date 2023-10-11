import math


# I'm not really sure what I'm doing for the stochastic method, as things don't seem very clear. Now I wish I paid
# attention during the previous class. Whatever, I'll pay attention on Monday, when people will hopefully ask questions
# But either way, I definitely need a fitness function, where I determine how good any given solution is
# So, let's start by writing that
# All I need to do is determine the number of conflicts in the set
def fitness_function(columns):
    # there are no vertical conflicts by the definition of the data structure
    # to check horizontal conflicts, we start by checking if there are any duplicate rows
    # The number of distinct rows is, let's see
    # If we have 6 distinct rows, that means that there were 2 more rows that had duplicates
    # Each of those is a conflict with 1 regular row, which means that the difference is num-conflicts
    # Only, that's not really true, because if there are multiple in the same row, it's a much bigger conflict
    # But I think I will ignore those. I don't think it really makes a difference for how bad it is

    side_length = len(columns)
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
    return sum(math.comb(duplicates, 2) for duplicates in row_nums.values())


'''
There has got to be a better way to find diagonal conflicts. Right now, my only way is to search through the diagonals
of every single row, which is n^2 time. Is there some better way?
Yes, there is. I could subtract each queen by... hold on, let me draw it.
'''


def unit_test_fitness(board, expected):
    print("Testing board " + str(board))
    result = fitness_function(board)
    if expected == result:
        print("Test success!")
    else:
        print("Test failed: expected " + str(expected) + " but received " + str(result))


'''
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
