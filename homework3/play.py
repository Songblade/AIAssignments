import alphaBetaPrunning
import game
board = game.create()
game.whoIsFirst(board)

# I removed oneMoreChance. It's always false, so if I replace it with False, it shouldn't matter
# But it will make it easier to figure out what this does
while not game.isFinished(board):
    if game.isHumTurn(board):
        game.inputMove(board)
    else:
        board = alphaBetaPrunning.go(board)
    if game.isFinished(board):
        # I think that anyLegalMove in this case is supposed to change players if the other play can still do something
        # But I don't think that it actually does that
        if game.anyLegalMove(board):
            print("No more moves - One more chance")
            game.changePlayer(board)

game.printState(board)

