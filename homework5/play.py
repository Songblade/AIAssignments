import game

board = game.game()
game.create(board)
print("Initial Game")
game.printState(board)
game.decideWhoIsFirst(board)
comp_count = 0
for i in range(0, 100):  # This loops takes about 15 seconds on my computer
    while not game.isFinished(board):
        if game.isHumTurn(board):  # The simple agent plays "Human"
            # NOTE: Whenever you change the opponent here, also change it in the MC simulation
            # game.inputMove(board)
            game.inputHeuristic(board)
            # game.inputRandom(board)
        else:
            game.inputMC(board)  # The MC agent plays "Computer"
        game.printState(board)
    if game.value(board) == 10**20:  # the MC Agent won
        comp_count += 1
    print("Start another game")
    game.create(board)
print("The MC agent beat the baseline:", comp_count, " out of ", i + 1)

# Against Random: The MC agent beat the baseline: 97  out of  100
# But against Heuristic: The MC agent beat the baseline: 73  out of  100
