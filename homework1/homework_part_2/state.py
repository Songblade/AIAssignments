'''
The state is a list of 2 items: the board, the path
The target for 8-puzzle is: (zero is the hole)
012
345
678
'''
import random
import math


# returns a random board nXn
def create(n):
    s = list(range(n*n))      # s is the board itself. a vector that represent a matrix. s=[0,1,2....n^2-1]
    m = "<>v^"                # m is "<>v^" - for every possible move (left, right, down, up)
    for i in range(n*n*n):  # makes n^3 random moves
        if_legal(s, m[random.randrange(4)])
    return [s, ""]           # at the beginning "" is an empty path, later on path
    # contains the path that leads from the initial state to the state


def get_next(x):            # returns a list of the children states of x
    ns = []                   # the next state list
    for i in "<>v^":
        s = x[0][:]           # [:] - copies the board in x[0]
        if_legal(s, i)       # try to move in direction i
        # checks if the move was legal and...
        if s.index(0) != x[0].index(0) and \
           (x[1] == "" or x[1][-1] != "><^v"["<>v^".index(i)]):  # check if it's the first move or it's a reverse move
            ns.append([s, x[1]+i])   # appends the new state to ns
    return ns


def path_len(x):
    return len(x[1])


def is_target(x):
    n = len(x[0])                     # the size of the board
    return x[0] == list(range(n))     # list(range(n)) is the target state


#############################
def if_legal(x, m):                  # gets a board and a move and makes the move if it's legal
    n = int(math.sqrt(len(x)))        # the size of the board is nXn
    z = x.index(0)                    # z is the place of the empty tile (0)
    if z % n > 0 and m == "<":            # checks if the empty tile is not in the first col and the move is to the left
        x[z] = x[z-1]                 # swap x[z] and x[z-1]...
        x[z-1] = 0                    # ...and move the empty tile to the left
    elif z % n < n-1 and m == ">":        # check if the empty tile is not in the n's col and the move is to the right
        x[z] = x[z+1]
        x[z+1] = 0
    elif z >= n and m == "^":           # check if the empty tile is not in the first row and the move is up
        x[z] = x[z-n]
        x[z-n] = 0
    elif z < n*n-n and m == "v":        # check if the empty tile is not in the n's row and the move is down
        x[z] = x[z+n]
        x[z+n] = 0


def hdistance(s):  # This is uniform cost and not based on any heuristic
    return 0


def hdistance1(s):  # This will be the simple heuristic of the number of bricks not in place
    return sum(1 for correct_piece, real_piece in enumerate(s[0]) if correct_piece != real_piece and real_piece != 0)


def hdistance2(s):  # This will be the Manhattan distance heuristic
    # for each index, I need to figure out how far the piece that's there is from its intended spot
    # unless it's 0, in which case I ignore it, because that might not be admissible
    # Let's see. We know that if real == intended, we add 0
    # If it is supposed to be on the same level:
    # Then we just return the absolute value of the difference
    # Say, it is in 0, but should be in 3, we need to move it 3 spaces, or vice versa
    # But, if it is supposed to be on a different level but in this spot
    # For example, in a 4x4 board, it should be in 12, but it's in 0
    # We need to move it by 3 spots, which is 12 / 4
    # Let's say it was in 3 but needed to be in 15
    # We move it (15-3)/4 spots, which is 3, as it should be
    # So, we get vertical distance by doing abs(real-supposed)/n
    # So, how do we combine this? What if it is in 0 but should be in 15?
    # We need to move it 6 - 3 horizontally, 3 vertically
    # So, would that be difference // n + difference % n?
    # Let's see. The difference is 15. 15 // 4 == 3, 15 % 4 == 3
    # Given another case: We need to move something from 1 to 14, should be 4
    # The difference is 13
    # Divided by 4, we get 3 remainder 1, which sums up to get 4, as we expected
    # And I should be able to do it in the same sum block
    # Correction: Calculate the row and column for each, modding and dividing separately, and then compare
    n = int(math.sqrt(len(s[0])))
    return sum(abs(correct_piece // n - real_piece // n) + abs(correct_piece % n - real_piece % n)
               for correct_piece, real_piece in enumerate(s[0]) if real_piece != 0)
