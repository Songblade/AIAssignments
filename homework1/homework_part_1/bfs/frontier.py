# implements a queue
# [head, tail, num_inserts, num_deletes] - the first and last items on a linked list
# num_inserts is the number of times that something was inserted to the list, num_deletes is the number of times
# something was removed
# inserts to the tail and removes from the head
# every item is [value, next_item]

# s is the puzzle board state
# Contains an array that contains 2 identical arrays, each with the board state in one index and the next null
# because they are both the head and tail of the 1-item queue
def create(s):
    p = [s, None]
    return [p, p, 1, 0]

def is_empty(f):
    return f[0] is None

# f is the frontier queue, s is the puzzle state
def insert(f, s):
    #inserts state s to the frontier
    p = [s, None] #New item
    if is_empty(f):
        f[0] = p #The head points to the new item
        f[1] = p #The tail points to the new item
    else:
        f[1][1] = p #Connects the last item to the new item
        f[1] = p    #The tail points to the new item
    f[2] += 1 # we add another state, because we added one

def remove(f):
    if is_empty(f):
        return 0
    p = f[0][0] #value of the item at the head of the queue
    f[0] = f[0][1] #Moves the head to the next item
    if f[0] is None: #If the head is None
        f[1] = None  #the tail should also be None
    f[3] += 1  # Because we removed a state, we add a state
    return p

