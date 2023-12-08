import copy
import random

VICTORY = 10**20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE+1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
random.seed()

rows = 6
columns = 7


class game:
    board = []
    size = rows*columns
    playTurn = HUMAN

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


def create(s):
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows):
        s.board = s.board+[columns*[0]]

    s.playTurn = HUMAN
    s.size = rows*columns
    s.val = 0.00001


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2


def value(s):
    # Returns the heuristic value of s
    dr = [-SIZE+1, -SIZE+1, 0, SIZE-1]  # the next lines compute the heuristic val.
    dc = [0, SIZE-1, SIZE-1, SIZE-1]
    val = 0.00001
    for row in range(rows):
        for col in range(columns):
            for i in range(len(dr)):  # basically, range(len(dr)) means range(4) in fancy-speak
                t = checkSeq(s, row, col, row+dr[i], col+dc[i])
                if t in [LOSS, VICTORY]:
                    return t  # Since we have a loss or a victory, we can just return it without any problem with our
                    # algorithm, which should make this faster
                else:
                    val += t
    if s.size == 0 and val not in [LOSS, VICTORY]:
        val = TIE
    return val


def checkSeq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
        return 0  # r2, c2 are illegal

    dr = (r2-r1)//(SIZE-1)  # the horizontal step from cell to cell
    dc = (c2-c1)//(SIZE-1)  # the vertical step from cell to cell

    sum = 0

    for i in range(SIZE):  # summing the values in the seq.
        sum += s.board[r1+i*dr][c1+i*dc]

    if sum == COMPUTER*SIZE:
        return VICTORY

    elif sum == HUMAN*SIZE:
        return LOSS
    elif 0 < sum < COMPUTER:
        return -1

    elif sum > 0 and sum % COMPUTER == 0:
        return 1
    return 0.00001  # not 0 because TIE is 0


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print("X|", end="")
            elif s.board[r][c] == HUMAN:
                print("O|", end="")
            else:
                print(" |", end="")
    print()

    for i in range(columns):  # For numbers on the bottom
        print(" ", i, sep="", end="")

    print()

    # Since we only care about VICTORY, LOSS, or TIE, I'm using finish_value for efficiency
    val = finish_value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!")
    elif val == TIE:
        print("It's a TIE")


def isFinished(s):
    # returns True iff the game ended
    # I replaced value with a more efficient function that only returns LOSS, VICTORY, TIE, or a placeholder
    # and doesn't act as a heuristic
    # to make my games faster, though I'm not sure that it changed anything
    return finish_value(s) in [LOSS, VICTORY, TIE]  # I got rid of "or size == 0", because if size == 0, then value
    # returns TIE


# Note: For efficiency, I replaced all equations of constants with their actual values
# To see where they came from, look at the full version of value
# this version only returns VICTORY, LOSS, TIE, or 0.00001 as a placeholder
def finish_value(s):
    # Returns the heuristic value of s
    dr = [-3, -3, 0, 3]  # the next lines compute the heuristic val.
    dc = [0, 3, 3, 3]
    for row in range(rows):
        for col in range(columns):
            if s.board[row][col] != 0:
                # if it equals 0, there's no piece here, so it definitely isn't part of a winning streak
                for end_row, end_col in zip(dr, dc):
                    # going through dr and dc directly, without checking the index
                    # might not make it better, but won't make it worse
                    t = finish_check_seq(s, row, col, row+end_row, col+end_col)
                    if t in [LOSS, VICTORY]:
                        return t
    return TIE if s.size == 0 else 0.00001


def finish_check_seq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # Otherwise, returns 0.00001.
    # I got rid of c2 < 0, since it is always >= c1
    if r2 < 0 or r2 >= rows or c2 >= columns:
        return 0  # r2, c2 are illegal

    dr = (r2-r1) // 3  # the horizontal step from cell to cell
    dc = (c2-c1) // 3  # the vertical step from cell to cell

    val_sum = 0
    for i in range(SIZE):  # summing the values in the seq.
        val_sum += s.board[r1+i*dr][c1+i*dc]
    # I have no idea if this one-line version is more efficient, but it certainly isn't less efficient
    return VICTORY if val_sum == 20 \
        else LOSS if val_sum == 4 \
        else 0.0001


def isHumTurn(s):
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


# I edited this to let me specify who goes first in the code
def decideWhoIsFirst(s, first="manual"):
    # The user decides who plays first
    if first == "manual":
        if int(input("Who plays first? 1-MC / anything else-you : ")) == 1:
            s.playTurn = COMPUTER
        else:
            s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER if first == "computer" else HUMAN
    return s.playTurn


def makeMove(s, c):
    # Puts mark (for human or computer) in col. c
    # and switches turns.
    # Assumes the move is legal.
    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r-1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    s.playTurn = HUMAN if s.playTurn == COMPUTER else COMPUTER  # reducing jumps


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
        else:
            flag = False
            makeMove(s, c)


def inputRandom(s):
    # See if the agent can win block one move ahead
    for i in range(0, columns):  # this simple agent always plays min
        # if we already have a full column, we shouldn't be looking at it
        if s.board[0][i] == 0:
            tmp = cpy(s)
            makeMove(tmp, i)
            # since we only check if value is LOSS, I replaced it with finish_value for efficiency
            if finish_value(tmp) == LOSS and s.board[0][i] == 0:  # if the agent should win
                makeMove(s, i)
                return
    # If no obvious move, then move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if not (c < 0 or c >= columns or s.board[0][c] != 0):
            flag = False
            makeMove(s, c)


def inputHeuristic(s):
    # See if the agent can win or get more than one in a row
    temp = 1000
    tmp_col = 0
    for i in range(0, columns):  # this simple agent always plays min
        # if we already have a full column, we shouldn't be looking at it
        if s.board[0][i] == 0:
            tmp = cpy(s)
            makeMove(tmp, i)
            if value(tmp) < temp and s.board[0][i] == 0:  # so a "loss" is a win for this side
                tmp_col = i
                temp = value(tmp)
    makeMove(s, tmp_col)


# If you are wondering, my main efficiency change was in finish_value, where I only run finish_check_seq on a starting
# position that isn't 0, since it couldn't have a win, loss, or tie
# But I couldn't make that change for the full version of value, because that would mess up the heuristic
# But here, we don't care about the heuristic
def inputMC(s):
    # inputHeuristic(s)
    # '''
    num_plays = 100

    best_move = -1
    best_wins = -1
    for move in range(columns):
        if s.board[0][move] == 0:
            # No point in investigating the move if it's out of bounds
            # We get the number of victories playing 100 games
            num_victories = sum(
                (play_game_from_move(s, move) for _ in range(num_plays))
            )
            # no point in calculating win rate
            # since we play 100 games for every move, we can just compare the raw number of victories
            if num_victories > best_wins:
                best_wins = num_victories
                best_move = move

    # finally, we actually make the move we have determined is best
    makeMove(s, best_move)
    # also, print the board, at least for debugging, so I know my progress
    # printState(s)
    # '''


# this function clones the board and plays a game from this move
def play_game_from_move(state, move):
    new_state = cpy(state)
    makeMove(new_state, move)

    while not isFinished(new_state):
        # It doesn't matter whose turn it is, make a random move until we can't
        column = random.randrange(0, columns)
        if new_state.board[0][column] == 0:
            makeMove(new_state, column)
            # If not, try again with a different random value
            # I determined that keeping track of which rows are open is too expensive
    end_state = finish_value(new_state)
    return 1 if end_state == VICTORY else 0 if end_state == LOSS else 0.5  # 1 means the MC agent won, 0 means it lost
    # 0.5 means it tied, since there is no other possibility
    # I think it leads to a slight increase in win rate, though it might not be statistically significant
