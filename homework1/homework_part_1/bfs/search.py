#search
import state
import frontier
import time


def search(n):
    start_time = time.time()
    s = state.create(n)
    # print(s)
    f = frontier.create(s)

    while not frontier.is_empty(f):
        s = frontier.remove(f)
        elapsed_time = time.time() - start_time
        # you said that if any execution takes more than 5 seconds, we should end it and give large numbers
        # specifically, you suggested Average depth = 20, Average number inserted / removed = 10000, runtime=100 seconds
        # But, the longest attempts, still less than 5 seconds on my machine, have 1345817 inserts and 631681 deletes
        # And average depth was nearly 15, close to 20
        # So, I decided to consider average depth 25, inserts 1500000, and removes 700000

        if elapsed_time > 5:
            return [0, "abcdefghijklmnopqrstuvwxy"], 700000, 700000, 100

        if state.is_target(s):
            # I have made the method also return the number of items inserted, removed, and the runtime
            return s, f[2], f[3], elapsed_time
        ns=state.get_next(s)
        for i in ns:
            frontier.insert(f, i)

    return 0

# Apparently, importing a module means running every line of code in it
# So the existence of a print here is messing things up
#  print(search(4))


