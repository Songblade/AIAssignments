#search

import state
import frontier
import time


def search(n, heuristic):
    start_time = time.time()
    s = state.create(n)
    # print(s)
    f = frontier.create(s, heuristic)
    while not frontier.is_empty(f):
        s = frontier.remove(f)
        elapsed_time = time.time() - start_time
        # you said that if any execution takes more than 5 seconds, we should end it and give large numbers
        # specifically, you suggested Average depth = 20, Average number inserted / removed = 10000, runtime=100 seconds
        # But, the longest attempts, still less than 5 seconds on my machine, have 1345817 inserts and 631681 deletes
        # And average depth was nearly 15, close to 20
        # So, I decided to consider average depth 25, inserts 1500000, and removes 700000

        if elapsed_time > 5:
            return [0, "abcdefghijklmnopqrstuvwxy"], 1500000, 700000, 100

        if state.is_target(s):
            return [s, f[1], f[3], elapsed_time]
        ns = state.get_next(s)
        for i in ns:
            frontier.insert(f, i)
    return 0


# print(search(4, state.hdistance2))

