import game
import time


# opponent is the opponent you are playing, either inputRandom, inputHeuristic, or inputMove
def run_simulation(opponent_move, first="manual"):
    board = game.game()
    game.create(board)
    print("Initial Game")
    # game.printState(board)
    game.decideWhoIsFirst(board, first)
    start_time = time.time()
    comp_count = 0
    for i in range(0, 100):  # This loops takes about 15 seconds on my computer
        while not game.isFinished(board):
            if game.isHumTurn(board):  # The simple agent plays "Human"
                opponent_move(board)
            else:
                game.inputMC(board)  # The MC agent plays "Computer"
            # game.printState(board)
        if game.value(board) == 10**20:  # the MC Agent won
            comp_count += 1
        # print("Game", i + 1, "is complete at time", time.time() - start_time, "with a ratio of", comp_count, "out of",
        # i + 1)
        game.create(board)
    print("The MC agent beat the baseline:", comp_count, "out of", i + 1)
    print("Elapsed time is", time.time() - start_time, "when the max is 600")


# Against Random: The MC agent beat the baseline: 97  out of  100
run_simulation(game.inputRandom, "computer")
# Against Heuristic: The MC agent beat the baseline: 85 out of 100
run_simulation(game.inputHeuristic, "computer")
# Time against Heuristic: 697.2819616794586 seconds
