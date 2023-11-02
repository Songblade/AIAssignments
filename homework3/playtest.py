import game
import alphaBetaPrunning
import dummy_game


def select_who_is_first():
    first_player = input("Will your algorithm go first or the stupid one?" "\n" "Print 'mine' for yours to go first: ")
    if first_player == 'mine':
        board[2] = game.COMPUTER
    else:
        board[2] = game.HUMAN


# the purpose of this file is to be able to test algorithms with it.
# It contains the mechanisms to play against a computer

answer = input("Print 'yes' to test your algorithm, play as human otherwise: ")


if answer != 'yes':
    import play
    # and do everything in the module
    # I'm not sure why it's greyed out in my IDE
else:
    board = game.create()
    select_who_is_first()
    while not game.isFinished(board):
        if game.isHumTurn(board):
            board = dummy_game.go(board)
        else:
            game.printState(board)
            board = alphaBetaPrunning.go(board)

    winner = game.whoWin(board)
    game.printState(board)
    # print(board)
    if winner == game.VIC:
        print("Congratulations. The algorithm won!")
    elif winner == game.LOSS:
        print("Uh oh. The algorithm lost.")
    else:
        print("It was a tie.")

# Note: It took 1:32 for best algorithm going first, and 0:46 second
# While the simpler algorithm takes 0:58 going first, and 0:35 second
# When using the best algorithm against the dummy is 0:59 going first, and 1:06 on second
# Against the random dummy, it gets about 1:08. The worst I measured 1:48
