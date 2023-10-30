import copy

EMPTY, BLACK, WHITE = '.', '●', '○'
HUMAN, COMPUTER = '●', '○'

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
VIC = 10000000  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. flag to end game
'''


# The user decides who plays first
def whoIsFirst(s):
    global HUMAN, COMPUTER

    going_first = input("Would you like to go first or second?" "\n" "Print 'first' or 'second': ")
    if going_first.lower() == "second":
        s[2] = COMPUTER
    else:
        s[2] = HUMAN

    return s


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[2] == HUMAN


def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


# The HUMAN plays first (=BLACK)
def create():
    global HUMAN, COMPUTER
    board = [EMPTY] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    HUMAN, COMPUTER = '●', '○'
    return [board, 0.00001, HUMAN, False]


def printState(s):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(s[0][begin:end]))
    print(rep)

    if s[1] == VIC:
        print("Ha ha ha I won!")
    elif s[1] == LOSS:
        print("You did it!")
    elif s[1] == TIE:
        print("It's a TIE")


def inputMove(s):
    # Reads, enforces legality and executes the user's move.

    flag = True
    while flag:
        printState(s)
        move = int(
            input("To make your move enter a two digits number, the first number is row and the second is column" "\n"
                  "For example: if you want to choose the first row and the third column enter 13" "\n"
                  "Enter your next move: "))
        if not isLegal(move, s):
            print("Illegal move.")
        else:
            flag = False
            makeMove(move, s)


def value(s):
    # Returns the heuristic value of s
    s[1] = 1  # ## your code here ###
    return s[1]


def isFinished(s):
    # Returns True if the game ended

    # I probably don't need to worry about O(n^2), because I bet alphaBetaPruning is similarly bad
    # Question is how to actually do that
    # For whoever's turn it is, I need to check to see if they have any moves
    # So, I traverse the board searching for blanks
    # For each adjacent blank, I need to check if, on any side or corner, there is a piece of the opposite color
    # If there is, then we progress on that line. If we see a piece of the opposite color again, we progress.
    # If we see a piece of our color, we return false.
    # If we see a blank, then this line is a dud.
    # When we try every line

    # But hold on. This makes no sense. We already have a method that checks exactly what I described called
    # anyLegalMoves, which we call if this fails.
    # So I need to trace the code
    # If the game is finished and there isn't another chance:
    # If anyLegalMove returns true, which means that we still have a legal move:
    # Then we print that we have one more chance and change player, which we normally only do after a move is made.
    # If we don't have any legal moves, oneMoreChance is made false
    # Hold on. I don't know why oneMoreChance is even here. It doesn't do anything. It is always false and never made
    # true. This is stupid.

    # Yes, this is stupid. I'm just going to ignore all his code and do things my way, because his way doesn't make any
    # sense.
    # So, what do I want? At the beginning of each loop, we check if the game is finished. If the player has no more
    # moves, then we say one more chance and flip it to the opponent. If that player can't do anything either, the game
    # is over.
    # Meanwhile, if that player can do something:

    # Okay. I just did some research. I have absolutely no idea what one-more-chance actually means. According to
    # Wikipedia, there is no one more chance, and if one player can't make a move, they just pass. But the next player
    # can keep playing either until the other player can make moves again or no one can.

    # Okay. Now I know that anyLegalMove checks if there is any legal move for the current player.
    # Since he explicitly said that we don't need to worry if this player can't go but the other one can't,
    # All I need to do to determine isFinished is call anyLegalMove
    # That makes this function completely redundant, but that's the professor's fault in play.py
    return not anyLegalMove(s)


# returns true if the move is legal for the current player, false otherwise
def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)
    return s[0][move] == EMPTY and any(map(hasbracket, DIRECTIONS))


# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in squares() if isLegal(sq, s)]


# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in squares())
    if not isAny:
        s[3] = True
    return isAny


def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction


def changePlayer(s):
    if s[2] == COMPUTER:
        s[2] = HUMAN
    else:
        s[2] = COMPUTER


def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    value(s)
    changePlayer(s)
    return s


def whoWin(s):
    computerScore = 0
    humanScore = 0
    for sq in squares():
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if computerScore > humanScore:
        return VIC

    elif computerScore < humanScore:
        return LOSS

    elif computerScore == HUMAN:
        return TIE

    return 0.00001  # not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in squares()


# This function takes a square and a direction from that square. It checks if pieces are arranged in that direction
# such that this square is a flanking move from that direction
# If the square is a valid move from this direction, it returns the other square of your color you are flanking with
# Otherwise, it returns None
def findBracket(square, s, direction):
    bracket = square + direction
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
    return None if s[0][bracket] in (EMPTY) else bracket


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for m in legalMoves(s):
        tmp = copy.deepcopy(s)
        makeMove(m, tmp)
        ns += [tmp]
    return ns
