'''
implements a priority queue using a minimum heap
the heap is represented by a list
the parent of index i is in index (i-1)//2
the left child of index i is in index 2i+1
the right side of index i is in index 2i+2
'''
import state


# implements a priority queue
# [list of states, total num of states, heuristic function, number of states removed]
def create(s, heuristic):  # I made the returned queue start with a number of additions equal to 1,
    # because the first state was added
    return [[s], 1, heuristic, 0]


def is_empty(f):
    return f == []    # returns true iff f is empty list


def insert(h, s):
    # inserts state s to the frontier
    f = h[0]
    h[1] += 1
    f.append(s)     # inserts the new state as the last item
    i = len(f)-1      # i gets its value
    # move the item with smallest value to the root
    while i > 0 and val(f[i], h[2]) < val(f[(i-1)//2], h[2]):
        # while item i's value is smaller than the value of his father, swap!
        # the next three lines swap i and his father
        t = f[i]
        f[i] = f[(i-1)//2]
        f[(i-1)//2] = t
        i = (i-1)//2  # i moves upwards


def remove(h):
    if is_empty(h):
        return 0
    h[3] += 1
    f = h[0]
    s = f[0]
    f[0] = f[len(f)-1]    # the last leaf becomes the root
    del f[-1]       # delete the last leaf
    heapify(f, 0, h[2])    # fixing the heap
    return s


def val(s, heuristic):  # returns f(x) which is path len + heuristic distance from target
    return heuristic(s) + state.path_len(s)  # heuristic(s) calls whichever heuristic function was put in
'''
for greedy best first search val returns hdistance
for uniform cost val returns path len
'''


def heapify(f, i, heuristic):   # fix the heap by rolling down from index i
    # compares f[i] with its children
    # if f[i] is bigger than at least one of its children
    # f[i] and its smallest child are swapped
    min_son = i    # define i as min_son
    if 2*i+1 < len(f) and val(f[2*i+1], heuristic) < val(f[min_son], heuristic):   # if f[i] has a left son
        # and its left son is smaller than f[i]
        min_son = 2*i+1                    # define the left son as min_son
    if 2*i+2 < len(f) and val(f[2*i+2], heuristic) < val(f[min_son], heuristic):   # if f[i] has a right son
        # and its right son is smaller than f[min_son]
        min_son = 2*i+2                    # define the right son as min_son
    if min_son != i:                       # if f[i] is bigger than one of its sons
        t = f[min_son]                     # swap f[i] with the smaller son
        f[min_son] = f[i]
        f[i] = t
        heapify(f, min_son, heuristic)              # repeat recursively

        

        

    

