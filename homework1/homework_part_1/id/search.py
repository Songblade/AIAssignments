#search

import state
import frontier

def search(n):
    s=state.create(n)
    print(s)
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        if state.is_target(s):
            return [s, f[1]]
        ns=state.get_next(s)
        #print(ns)
        for i in ns:
            frontier.insert(f,i)
    return 0

answer=search(3)
print(answer)
