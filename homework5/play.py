import game
import time

board = game.game()
game.create(board)
print("Initial Game")
game.printState(board)
game.decideWhoIsFirst(board)
start_time = time.time()
comp_count = 0
for i in range(0, 100):  # This loops takes about 15 seconds on my computer
    while not game.isFinished(board):
        if game.isHumTurn(board):  # The simple agent plays "Human"
            # NOTE: Whenever you change the opponent here, also change it in the MC simulation
            # game.inputMove(board)
            # game.inputHeuristic(board)
            game.inputRandom(board)
        else:
            game.inputMC(board)  # The MC agent plays "Computer"
        # game.printState(board)
    if game.value(board) == 10**20:  # the MC Agent won
        comp_count += 1
    print("Game", i + 1, "is complete at time", time.time() - start_time, "with a ratio of", comp_count, "out of", i + 1)
    game.create(board)
print("The MC agent beat the baseline:", comp_count, "out of", i + 1)
print("Elapsed time is", time.time() - start_time, "when the max is 600")

# Against Random: The MC agent beat the baseline: 99  out of  100
# Against Heuristic: The MC agent beat the baseline: 83 out of 100
