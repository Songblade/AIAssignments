import copy
import game
import random

# this file contains the bad computer algorithm that I test my code against
DEPTH = 5


# I don't want to define this up here, but otherwise, it isn't referenced for some reason
def go(s):
    # this is the new version of dummy that always chooses a random legal move
    legal_moves = game.legalMoves(s)
    move = random.choice(legal_moves)
    make_move(move, s)
    return s
    '''  # Not code
    if game.isHumTurn(s):
        return ab_min(s, DEPTH, float("-inf"), float("inf"))[1]
    else:
        return ab_max(s, DEPTH, float("-inf"), float("inf"))[1] # '''


# Everything from here and below is the alpha-beta for the dummy
# Unfortunately, this doesn't use object-oriented design, so I don't know how to reuse the code, so I'm copy-pasting it
# s = the state (max's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recommended move.
#        if s is a terminal state ns=0.
def ab_max(s, d, a, b):
    if d == 0 or game.isFinished(s):
        return [value(s), 0]
    v = float("-inf")
    ns = get_next(s)
    best_move = 0
    for i in ns:
        tmp = ab_min(copy.deepcopy(i), d - 1, a, b)
        if tmp[0] > v:
            v = tmp[0]
            best_move = i
        if v >= b:
            return [v, i]
        if v > a:
            a = v
    return [v, best_move]


# s = the state (min's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recommended move.
#        if s is a terminal state ns=0.
def ab_min(s, d, a, b):
    if d == 0 or game.isFinished(s):
        return [game.value(s), 0]
    v = float("inf")
    ns = get_next(s)
    best_move = 0
    for i in ns:
        tmp = ab_max(copy.deepcopy(i), d - 1, a, b)
        if tmp[0] < v:
            v = tmp[0]
            best_move = i
        if v <= a:
            return [v, i]
        if v < b:
            b = v
    return [v, best_move]


def value(board):
    # return game.alt_value(board)
    # '''
    # Let's see. I want, for this simple one, to make corners worth 20, edges worth 5, and everything else worth 1
    # Of course, if one side wins, loses, or ties, that's still worth what you would expect
    if game.is_next_player_finished(board):  # if a player is out of moves, which we are treating as the end of the game
        # then the value is equal to victory, loss, or tie
        board[1] = game.whoWin(board)
    else:
        # We evaluate the board, considering HUMAN positions good, with center pieces worth 1,
        # edges worth 5, and corners 20
        board[1] = 0
        for square in game.squares():
            piece = board[0][square]
            if piece == game.COMPUTER:
                board[1] -= evaluate_position(square)  # because we don't want the computer doing well
            elif piece == game.HUMAN:
                board[1] += evaluate_position(square)

        if board[1] == game.TIE:
            board[1] = 0.00001

    return board[1]  # '''


# The evaluation uses negative values, because the human side (which this algorithm is playing for)
# uses negative numbers
def evaluate_position(square):
    if (square % 10 == 1 or square % 10 == 8) and (square // 10 == 1 or square // 10 == 8):
        return -119
    elif (square % 10 == 1 or square % 10 == 8) or (square // 10 == 1 or square // 10 == 8):
        return -17
    else:
        return -1


def get_next(s):
    # returns a list of the next states of s
    ns = []
    for m in game.legalMoves(s):
        tmp = copy.deepcopy(s)
        make_move(m, tmp)  # we use our make_move, because that uses our value
        ns += [tmp]
    return ns


def make_move(move, s):
    s[0][move] = s[2]
    for d in game.DIRECTIONS:
        game.makeFlips(move, s, d)
    value(s)  # we use our value function
    game.changePlayer(s)
    return s
