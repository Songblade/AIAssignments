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
                    val = t
                    break
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
    # to make my games faster
    return finish_value(s) in [LOSS, VICTORY, TIE] or s.size == 0


# Note: For efficiency, I replaced all equations of constants with their actual values
# To see where they came from, look at the full version of value
# this version only returns VICTORY, LOSS, TIE, or 0.00001 as a placeholder
def finish_value(s):
    # Returns the heuristic value of s
    dr = [-3, -3, 0, 3]  # the next lines compute the heuristic val.
    dc = [0, 3, 3, 3]
    for row in range(rows):
        for col in range(columns):
            for end_row, end_col in zip(dr, dc):
                # going through dr and dc directly, without checking the index
                # might not make it better, but won't make it worse
                t = finish_check_seq(s, row, col, row+end_row, col+end_col)
                if t in [LOSS, VICTORY]:
                    return t
    if s.size == 0:
        return TIE
    return 0.00001


'''
Okay. Let's see if I can't make value more efficient. Right now, we use this every loop, so it's really the most
important, given that it has triply nested loops inside of it. If I could reduce the length of dr and dc by even 1, it
would make the program much faster. So, can I do that?

Given any piece in Connect 4, we could check every sequence by checking the sequence to the right, the sequence above,
and the sequence diagonally. The piece could be in more sequences than that, but if it is, we would be able to find out
from the beginning of those sequences. But, we are looking at 4 of them. What's the fourth?

Let's see. The first is row -SIZE + 1, column 0. So, row -3, column 0. This is checking for the sequence below (which 
is really above, because the board is stored upside down).

Next we have row -SIZE + 1, column SIZE-1. Row -3, column 3. So, diagonal up-right.

Wait, I just realized why we need 4 of them. Because there are two diagonals. There is diagonal up-left and up-right. If
we only check one, we will never check the other. So, we really do need to check all of them.

Hmm. Looking at this, I could probably make a streamlined version for isFinished. When it's used in inputHeuristic, it
really needs all the stuff. But for isFinished, all we care about is if it's WIN, LOSS, or TIE. So, we can remove all
code that calculates the heuristic when making a special version for isFinished.

That doesn't seem to have notably improved efficiency. Maybe I just didn't trim enough to make a significant difference.
'''


def finish_check_seq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
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


def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-MC / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN
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
    if s.playTurn == COMPUTER:
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


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


def inputMC(s):
    # inputHeuristic(s)
    # '''
    num_plays = 100

    best_move = -1
    best_wins = -1
    for move in range(columns):
        if s.board[0][move] == 0:
            # No point in investigating the move if it's out of bounds
            num_victories = sum(
                (play_game_from_move(s, move) for _ in range(num_plays))
            )
            if num_victories > best_wins:
                best_wins = num_victories
                best_move = move

    # finally, we actually make the move we have determined is best
    makeMove(s, best_move)
    # also, print the board, at least for debugging, so I know my progress
    # printState(s)
    # '''


def play_game_from_move(state, move):
    # this function clones the board and plays a game from this move
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


'''
Okay, so what am I doing wrong? Not only is my algorithm taking too long, it also isn't good enough. Taking too long by
itself isn't a problem, because I could probably get more efficiency by running the games in parallel. What is a problem
is that it's not good enough. That I have both problems suggests that they are connected. Or if not, I could make it
parallel after solving the first problem.

So, what am I doing wrong? I think I am solving the problem as well as he wants us to. But clearly, I'm not.

Okay, I just found a bug, but solving it seems to have made it worse. I think it's because I restricted it to legal
moves.

I fixed it so that the opponents are also restricted to legal moves, and it's all back to normal.

Anyway, it seems that I'm not the only one with problems. So, I'm going to ignore those and focus on how I can make this
faster.

Okay, so, what can I even fix? Let's start looking at my function only. If that doesn't work, I will try to optimize the
professor's code.

So, my top loop goes through every column. Since every column is an option, we need to look at all of them. The only 
time we know that we don't need to look at a column is when it's already full, which we are already doing. So, that's
not optimizable beyond parallelism.

Next loop: we play the game from that point 100 times. Since we need to play 100 games from that move, that can't really
be optimized. Meanwhile, calculating the win rate and comparing it to the best one can't really be optimized.

Okay, maybe I can optimize within the games. First, we copy the state. We can't use the old state, so we can't get
around that. Then, we make the starting move. Then, we have the loop of the game. For as long as we can, we perform
fully random moves for whichever side we happen to be. If that move is for a full column, we skip it. So, that seems to
be something perhaps I could optimize. Obviously, I can't let it make false moves. But, is there some other way I could
keep track of full columns?

I could add a check whenever I make a move to check if it fills a column. If it does, I make a note. I think I would
have an array with all legal moves. Whenever I fill a column, I remove it. Then, I take a random element of that array
as the column we go into.

If I'm keeping track of that, I could also make all iterations through the columns go through that array instead, which
wouldn't save all that much time, but is still interesting.

But would this save time? I would save a number of elements where the move is not available and - oh, this is big. I
wouldn't have to do the check every time. Except, that's not actually true. Instead of checking whether this move is
invalid, I would be checking if this move causes a column to be invalidated. So, it's just code motion. My only saving
is that I would be checking invalid columns. But that doesn't happen that much.

And it's at the cost that whenever I copy the board, I also have to copy this array, an O(n) operation. So, is it worth
it? Only if the number of bad moves is greater than the time to copy the board. Is it? If it's greater than 7, perhaps.
But I'm not so sure. Yeah, I don't think this will actually save any time. So, this isn't where I need to make a change.

Either way, I still want to make a change at the base of the loop. Here, even an O(1) improvement would be massive. And
I only make 2: isFinished and makeMove. So, those are what I need to modify.

Okay. The obvious inefficiency in makeMove is that we have to go through each row to check if that's the right one.
Would it make more sense to simply keep track of the value of each column? If so, I would have O(n) when copying to copy
the array, and I would need to increase the value by 1. The latter is O(1), and the former is O(n) every once in a
while. This is a great fix and I should implement it immediately.

Places to change:
create() should create this array and initialize it to 7 0s
cpy() should copy this array as well
makeMove() should check and update this array

Okay, why isn't my change more efficient? It should be, but it isn't. I've pretty clearly demonstrated that it's no
better than the alternative. So, how do I fix it?

Also, I have confirmation from Aryeh that it is possible to have a near-perfect run. So I have to figure out what I'm
doing wrong.

But let's start by examining my change. Maybe I made an error that makes it slower.

Maybe I can fix it by going further?

Hmm. Let's see if I can't boost win-rate with a better heuristic. Let's say that win is 1, loss is 0, and tie is 0.5.
It still wants the most amount of wins, but now would prefer ties over losses. Since in the end, I only care about
victories, this might not matter, but I should at least try it.

Okay. I got 87 / 100, which is better than I have gotten before. I suspect I got lucky, and the actual total is below
this. But it's certainly a fine start. And what Aryeh said implies that I don't actually need to reach the 90s. If I can
that would be great. But I should focus on reducing from nearly 1000 seconds to 600.

You know what. Let's determine the difference between his heuristics, to see how much each one actually takes. That
could help determine whether I need to increase mine or his. So, it took 997.6084713935852 seconds to complete my latest
set for heuristic. For Random, I instead take 

I have decided that calculating this is a waste of time. Maybe I will do it when I am going in and out. Also, I don't
know how I would interpret the data, since each result is the sum of the data I am looking for with my actual algorithm.
If I really wanted to, I could also get a third set of data, being my heuristic playing against itself. That would be
useless for the win rate (probably around 50%), but it would tell me the value of that variable, allowing me to
calculate the other.

But it looked like it was going to take about 800 seconds, maybe a bit more. So, 200 more seconds is a lot. Why is
heuristic taking so much longer?

Why didn't my old efficiency tool work? Maybe I need to be checking where everything is going. I've just been assuming
what's taking more time, but I could be wrong. But I really don't want to build such a framework.
'''
