'''
The state is a list of 2 items: the board, the path
The target is :
012
345
678

'''
import random
import math

#x is the current number puzzle state
def get_next(x):
    ns=[]
    for i in "<>v^":
        s=x[0][:]
        if_legal(s,i)
        if s.index(0)!=x[0].index(0) and \
           (x[1]=="" or x[1][-1]!="><^v"["<>v^".index(i)]):
            ns.append([s,x[1]+i])
    return ns

#returns a random board nXn
# the board contains the actual puzzle in index 0, a length n^2 1D array where the empty spot is represented as a 0
# At index 1, it contains the path, a String of moves used to bring the puzzle from its initial state to its current one
# moves are represented by ^ for up, < for left, > for right, and v for down
def create(n):
    s=list(range(n*n))
    m="<>v^"
    for i in range(n**3):
        if_legal(s,m[random.randrange(4)])
    return [s,""]

# given x, the current board state, it returns the length of the path used
def path_len(x):
    return len(x[1])

# checks if the given number puzzle is in its solution state
def is_target(x):
    n=len(x[0])
    return x[0]==list(range(n))

def hdistance(s):
    return 0

#############################
# checks if the proposed move is legal, given x, the board state, and m, the move
def if_legal(x,m):
    n=int(math.sqrt(len(x)))
    z=x.index(0)
    if z%n>0 and m=="<":
        x[z]=x[z-1]
        x[z-1]=0
    elif z%n<n-1 and m==">":
        x[z]=x[z+1]
        x[z+1]=0
    elif z>=n and m=="^":
        x[z]=x[z-n]
        x[z-n]=0
    elif z<n*n-n and m=="v":
        x[z]=x[z+n]
        x[z+n]=0

