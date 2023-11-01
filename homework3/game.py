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


'''
Heuristic documentation:

After playing 3 games of Othello against my 10-year-old brother (I only won the third time), I learned the following
strategy:

First, I decided on the relative worth of corners, edges, and other pieces. I gave regular pieces a value of 1. I
decided that an edge should always be worth more than a regular piece, no matter how many other regular pieces it flips.
I calculated that placing a regular piece could flip no more than 15 other pieces (best-case scenario), for 16 pieces
total. So I gave edges a value of 17, to always be better.

Likewise, a corner should always be better than an edge, no matter how many other edges the edge gets you. An edge can
flip no more than 5 other edges, for 6 edges total. So, I made the corners worth 7 edges, for 119 points total. I also
used these values for the dummy I use to test my code, which knows this and only this.

But playing against my little brother, I learned that certain positions are inherently dangerous, because they can (and
probably will) cause you to lose an edge or even a corner.

As such, I divided all the pieces on the board into 6 categories: corners, dangerous edges, safe edges, corner risks,
edge risks, and central pieces. Corners, safe edges, and central pieces all act like the corners, edges, and normal 
pieces that I described above.

Edge risks are normal pieces adjacent to edges. Since they could cause you to forfeit that edge, I gave them a negative
value of half the value of the edge that they are giving up. However, if you already have that edge, then they become
ordinary pieces.

Dangerous edges are edges adjacent to a corner that could cause you to forfeit that corner. As such, I gave them a
negative value of half the value of the corner that they are giving up. Once again, if you already have that corner,
then they become ordinary edges.

Corner risks are normal pieces diagonally connected to the corner (and adjacent to dangerous edges). They have a nasty
ability of forfeiting the corner, so I gave them a negative value of half the value of the corner that they are 
forfeiting. If you already have that corner, they become ordinary pieces.

If you think this is too complicated, I left in an earlier version of the heuristic as alt_value(). It still identifies
the dangerous pieces, but rather than figuring out if you already have the corner or edge it's guarding, I just gave the
piece half the value it would have had it been safe. This middling AI successfully beats my dummy, but it fails against
my superior AI. It is a bit faster, though. (The longest game I have recorded was just over a minute and a half, with my
superior AI playing against the middling one and the superior AI going first. It clocked in at just over a minute and a
half.)
'''


# These are the definitions of the groups of pieces that I used in my main value function
CORNERS = (11, 18, 81, 88)
DANGEROUS_EDGES = (12, 21, 17, 28, 71, 82, 78, 87)
SAFE_EDGES = (13, 14, 15, 16, 31, 41, 51, 61, 38, 48, 58, 68, 83, 84, 85, 86)
CORNER_RISKS = (22, 27, 72, 77)
EDGE_RISKS = (23, 24, 25, 26, 32, 42, 52, 62, 37, 47, 57, 67, 73, 74, 75, 76)
CENTRAL_PIECES = (33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66)


def value(s):
    # Returns the heuristic value of s
    if is_next_player_finished(s):  # if the next player is out of moves, which we are treating as the end of the game
        # then the value is equal to victory, loss, or tie
        # value is called immediately before changePlayer, so s[2] contains the player who just put down a piece
        s[1] = whoWin(s)
    else:  # if the game isn't over, evaluate according to my heuristic
        s[1] = 0
        computer_exception = set()
        human_exception = set()
        # first we check the corners, adding their value and noting if they make certain places safe
        for corner in CORNERS:
            piece = s[0][corner]
            if piece == COMPUTER:
                s[1] += 119
                computer_exception.update(corner + direction for direction in DIRECTIONS)
            elif piece == HUMAN:
                s[1] -= 119
                human_exception.update(corner + direction for direction in DIRECTIONS)
        # now we check the edge pieces that are adjacent to corners, either giving them a reverse value if they aren't
        # an exception or the normal edge value if they are
        for edge in DANGEROUS_EDGES:
            piece = s[0][edge]
            if piece == COMPUTER and edge in computer_exception:
                s[1] += 17
            elif piece == COMPUTER:
                s[1] -= 59.5  # since it could lead to losing a corner
            elif piece == HUMAN and edge in human_exception:
                s[1] -= 17  # since they have an edge
            elif piece == HUMAN:
                s[1] += 59.5  # because it could help us get a corner
        # now we check the extremely dangerous almost-corner pieces
        for square in CORNER_RISKS:
            piece = s[0][square]
            if piece == COMPUTER and square in computer_exception:
                s[1] += 1
            elif piece == COMPUTER:
                s[1] -= 59.5  # since it could lead to losing a corner
            elif piece == HUMAN and square in human_exception:
                s[1] -= 1  # since they have a piece
            elif piece == HUMAN:
                s[1] += 59.5  # because it could help us get a corner
        # Now we check the remaining 16 edges
        for edge in SAFE_EDGES:
            piece = s[0][edge]
            if piece == COMPUTER:
                s[1] += 17
                computer_exception.update(edge + direction for direction in DIRECTIONS)
            elif piece == HUMAN:
                s[1] -= 17
                human_exception.update(edge + direction for direction in DIRECTIONS)
        # now we check the remaining dangerous pieces that could lose an edge
        for square in EDGE_RISKS:
            piece = s[0][square]
            if piece == COMPUTER and square in computer_exception:
                s[1] += 1
            elif piece == COMPUTER:
                s[1] -= 8.5  # since it could lead to losing an edge
            elif piece == HUMAN and square in human_exception:
                s[1] -= 1  # since they have a piece
            elif piece == HUMAN:
                s[1] += 8.5  # because it could help us get an edge
        # finally, we add the regular squares
        for square in CENTRAL_PIECES:
            piece = s[0][square]
            if piece == COMPUTER:
                s[1] += 1
            elif piece == HUMAN:
                s[1] -= 1

        # if s[1] == TIE, but it isn't a tie because the game isn't over, we replace it with a very small value
        # So that the game won't scream that it's a tie
        if s[1] == TIE:
            s[1] = 0.00001

    return s[1]


# Checks if the other player is finished, used in my heuristic
def is_next_player_finished(board):
    board[2] = COMPUTER if board[2] == HUMAN else HUMAN
    result = isFinished(board)
    board[2] = COMPUTER if board[2] == HUMAN else HUMAN
    return result


# I chose not to use this, but if you don't like my primary heuristic, this one is simpler and slightly faster,
# if inferior
# it simply makes dangerous moves have half the value that they would normally have
def alt_value(s):
    # Returns the heuristic value of s
    if isFinished(s):  # if a player is out of moves, which we are treating as the end of the game
        # then the value is equal to victory, loss, or tie
        # I have to check here, because otherwise it is only checked after value is done
        s[1] = whoWin(s)
    else:
        s[1] = 0
        for square in squares():
            piece = s[0][square]
            if piece == COMPUTER:
                s[1] += evaluate_position(square)
            elif piece == HUMAN:
                s[1] -= evaluate_position(square)

        # if s[1] == TIE, but it isn't a tie because the game isn't over, we replace it with a very small value
        # So that the game won't scream that it's a tie
        if s[1] == TIE:
            s[1] = 0.00001

    return s[1]


# returns a number that says how valuable any given square is
def evaluate_position(square):
    danger_zone = (square % 10 in (1, 2, 7, 8) and square // 10 in (1, 2, 7, 8)) or ((square % 10 == 2 or square % 10 == 7) or (square // 10 == 2 or square // 10 == 7))
    if (square % 10 == 1 or square % 10 == 8) and (square // 10 == 1 or square // 10 == 8):  # corner piece
        return 119
    elif (square % 10 == 1 or square % 10 == 8) or (square // 10 == 1 or square // 10 == 8):  # edge piece
        return 17 if not danger_zone else 8.5
    else:  # central piece
        return 1 if not danger_zone else 0.5


def isFinished(s):
    # Returns True if the game ended

    # I mostly just used the code in anyLegalMove, which already basically does this
    # but anyLegalMove only does this if is_any is false, which is why I didn't call it
    is_any = any(isLegal(sq, s) for sq in squares())
    s[3] = not is_any
    return not is_any


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

    elif computerScore == humanScore:  # I found a bug. This should be computerScore == humanScore, but you did
        # computerScore == HUMAN, which is obviously false
        return TIE
    # why is this even here? It's impossible to reach!
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
