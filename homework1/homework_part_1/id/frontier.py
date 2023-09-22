import stack
import state


# [stack, max. depth, init. state, try next level?, total items pushed, total items removed]
def create(x):
    s = stack.create(x)
    return [s, 1, x, False, 1, 0]


def is_empty(s):
    return stack.is_empty(s[0]) and not s[3]  # stack is empty and try next level is false


def insert(s, x):
    if state.path_len(x) <= s[1]:  # check if x is not too deep
        stack.insert(s[0], x)      # insert x to stack
        s[4] += 1                  # Increment the number of states we have added to the stack
    else:
        s[3] = True                # there is a reason to search deeper if needed


def remove(s):
    if stack.is_empty(s[0]):    # check is there are no states in the stack
        if s[3]:                # check if there is a reason to search deeper
            s[1] += 1             # increase search depth
            s[3] = False          # meanwhile there is no evidence to need to search deeper
            # print(s[1])         # print what level we finished searching
            return s[2]         # return the initial state
            # I'm not counting returning this state as part of the count, since we have already returned it
            # and we never removed it from the stack
        else:
            return 0
    s[5] += 1  # if the stack isn't empty, and we remove a state, we should count that
    return stack.remove(s[0])   # if there are items in the stack ...

    
