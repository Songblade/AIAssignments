import queens_problem
import copy


'''
Okay. So, how do I implement this?
I need to keep track of which places we have pruned so that I don't go down paths I know won't work.
So, whenever I add a queen, I add its row and both diagonals to their respective sets
Whenever I check if I want to put a - hey, wait, this won't work. The entire point is to check when I know it will no
longer propagate.
So, either way, I would want a stack of board states.
But when I add a queen, I would go through its row and both diagonals and remove possibilities.
If we ever reach a state where a column's possibilities are all full, we know we made a mistake.
That will be my first attempt.

Let's see. How do I want to store my lookahead?
I am thinking of a 2D structure, where if a row is full (or empty, whichever I decide) then there are no more
possibilities for that row. Let's say when it's empty, so that if it isn't, we can iterate through it.
Each row should be a set, so that when we remove or check emptiness, it's an O(1) operation.
But the rows should be stored in a list so they can be indexed.
Actually, they should be in a dictionary, so that I can keep removing rows but have the remaining ones keep their value.
Actually, it will be simpler not to remove the rows, so let's keep it as a list.

Things to do:
Update the lookahead when we place a queen. When doing so, we also need to check if a row is no longer viable. If so,
we need to roll back this decision.
When we make a decision, we put the resulting lookahead on the stack. When we roll back a decision, we replace our 
lookahead with one from the stack. Although, actually, I don't need a stack. It will be simpler just to have an array.
So, when we make a decision, we add the old lookahead onto the array first for the row we just put a queen in.
Then, when we roll back a decision, we put take the old lookahead from the index we are rolling back to.
'''


def solve_queen(size):
    history = []  # stores the lookaheads that we are no longer using
    lookahead = [set(range(size)) for _ in range(size)]
    # Since making the lookahead isn't going through the board, it shouldn't count towards iterations

    columns = []

    number_of_moves = 0
    number_of_iterations = 0
    row = 0
    # I got rid of his column, because rather than going through the columns in his order, I go over them in whatever
    # order I pulled them out of the lookahead.
    # iterate over rows of board
    while True:
        # place queen in next row
        # print(columns)
        # print("I have ", row, " number of queens put down")
        # display()
        # print(number_of_moves)
        while row != 0 or len(lookahead[0]) != 0:  # while we are at the base but have no options, or we aren't at the
            # base
            number_of_iterations += 1
            number_of_moves += 1  # we placed a queen, so we count it
            # it's possible that we immediately remove it, but if so, we still placed it

            column = lookahead[row].pop()  # remove one move from the lookahead and try it
            # We don't need to check if it's safe, because if it weren't, it wouldn't be in the lookahead
            queens_problem.place_in_next_row(columns, column)
            if row == size - 1:  # This means that we have just put a queen in the last row
                # If we put it down, then it must be good, so we return
                print("I did it! Here is my solution")
                queens_problem.display(columns)
                # print(number_of_moves)
                return number_of_iterations, number_of_moves

            history.insert(row, copy.deepcopy(lookahead))  # we archive the lookahead, with its use recorded,
            # in case we need to go back to it.
            # We use deepcopy because we don't want any of our subsequent modifications to affect it
            lookahead, can_continue = update_lookahead(lookahead, row, column)
            row += 1  # If we are rolling back, we will subtract it back down anyway

            if not can_continue:  # We have a problem later on, so we need to roll back those changes
                # So we see how much we need to roll back
                while len(lookahead[row]) == 0 and row != 0:  # if this row in the lookahead is empty, we need to start
                    # rolling back to previous rows properly
                    row -= 1
                    lookahead = history[row]
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
    for row_number, lookahead_row in enumerate(lookahead[row + 1:], row + 1):
        # Only checking the rows that are after this one
        # We set enumerate to start its indices at that value, so that row_number will be accurate
        lookahead_row.discard(column)
        lookahead_row.discard(up_diagonal - row_number)
        lookahead_row.discard(row_number - down_diagonal)
        if len(lookahead_row) == 0:
            return lookahead, False  # This means that this is an invalid placement because of what it does later on
            # and we need to rollback

    return lookahead, True


'''
Something here is wrong with the rollback.
Let's say I was in row 4, and I did something that could cause problems in the future.
I want to rollback the changes, but I still want to be in row 4. I just want to be in the next part of row 4
But if I'm rolling back and row 4 is empty, then I want to roll back properly

Problem: It looks like the down diagonal doesn't work
So, I need to fix that
We are discarding row - down_diagonal
down_diagonal = row - column, or 0
So, we are discarding row - down_diagonal = 3 - 0 = 3
Hey, that should work.
Wait. I accidentally got confused between row and row_number due to bad naming conventions.
'''
