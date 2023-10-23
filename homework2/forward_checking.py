import queens_problem
import random


def solve_queen(size):

    past_moves = []  # stores the set of moves that we got rid of when we placed a queen in row i
    lookahead = [set(range(size)) for _ in range(size)]
    # Since making the lookahead isn't going through the board, it shouldn't count towards iterations

    columns = []

    number_of_moves = 0
    number_of_iterations = 0
    row = 0
    # I got rid of his column, because rather than going through the columns in his order, I go over them in whatever
    # order I pulled them out of the lookahead.

    # place queen in next row
    # print(columns)
    # print("I have ", row, " number of queens put down")
    # display()
    # print(number_of_moves)
    while row != 0 or len(lookahead[0]) != 0:  # while we are at the base but have no options, or we aren't at the base
        number_of_iterations += 1
        number_of_moves += 1  # we placed a queen, so we count it
        # it's possible that we immediately remove it, but if so, we still placed it
        column = random.sample(lookahead[row], 1)[0]
        lookahead[row].remove(column)
        # column = lookahead[row].pop()  # remove one move from the lookahead and try it
        # We don't need to check if it's safe, because if it weren't, it wouldn't be in the lookahead
        queens_problem.place_in_next_row(columns, column)

        if row == size - 1:  # This means that we have just put a queen in the last row
            # If we put it down, then it must be good, so we return
            # print("I did it! Here is my solution")
            # queens_problem.display(columns)
            # print(number_of_moves)
            return number_of_iterations, number_of_moves
        elif row != 0:
            past_moves[row - 1].add((row, column))  # We add the move we just put down to the reversing of the PREVIOUS
            # column
            # That way, we won't try the move again on this branch of the tree
            # But on a subsequent branch, it could become valid again, so we bring it back

        # in case we need to go back to it.
        # We use deepcopy because we don't want any of our subsequent modifications to affect it
        lookahead, set_of_moves, can_continue = update_lookahead(lookahead, row, column)
        past_moves.append(set_of_moves)
        row += 1  # If we are rolling back, we will subtract it back down anyway

        if not can_continue:  # We have a problem later on, so we need to roll back those changes
            # So we see how much we need to roll back
            while len(lookahead[row]) == 0 and row != 0:  # if this row in the lookahead is empty, we need to start
                # rolling back to previous rows properly
                row -= 1

                lookahead = revert_lookahead(lookahead, past_moves.pop())
                number_of_moves += 1
                queens_problem.remove_in_current_row(columns)
                # if row reaches 0 and len is 0, the bigger while loop will end
    # the while loop only ends if we have reached the base of the tree and have no moves left
    # So, this means that there is no solution
    print("There are no solutions")
    # print(number_of_moves)
    return number_of_iterations, number_of_moves


# When we select a column, we need to remove all conflicts from later on
# returns an updated lookahead if every subsequent row still has a value, False otherwise
# According to Piazza, when updating the lookahead, since we don't actually put anything on the board, we don't need
# to update our number of iterations here, which will likely lead to a strangely low number
def update_lookahead(lookahead, row, column):
    # I know the row+col or row-col that identifies the diagonal
    # So, I need to find the item in this row in the same one
    # So, if up_dia = row + col and I have up_dia and row, to get col, col = up_dia - row
    # Down_dia = row - col, -col = down_dia - row, col = row - down_dia
    up_diagonal = row + column
    down_diagonal = row - column
    set_of_moves = set()
    for row_number, lookahead_row in enumerate(lookahead[row + 1:], row + 1):
        # Only checking the rows that are after this one
        # We set enumerate to start its indices at that value, so that row_number will be accurate
        if column in lookahead_row:
            lookahead_row.remove(column)
            set_of_moves.add((row_number, column))

        up_column = up_diagonal - row_number
        if up_column in lookahead_row:
            lookahead_row.remove(up_column)
            set_of_moves.add((row_number, up_column))

        down_column = row_number - down_diagonal
        if down_column in lookahead_row:
            lookahead_row.remove(down_column)
            set_of_moves.add((row_number, down_column))

        if len(lookahead_row) == 0:
            return lookahead, set_of_moves, False  # This means that this is an invalid placement because of
            # what it does later on and we need to rollback

    return lookahead, set_of_moves, True


# This function takes every row-column tuple move in set_of_moves and adds it back to the lookahead
# Since we removed the queen that caused those moves to be off-limits
def revert_lookahead(lookahead, set_of_moves):
    for move in set_of_moves:
        lookahead[move[0]].add(move[1])
    return lookahead
