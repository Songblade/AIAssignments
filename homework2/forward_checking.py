import queens_problem
import random


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


'''
Problem: Everything is too slow. In order to fix that, I need to remove code in the innermost loop.
Looking at things, we have 3 innermost loops: deepcopy, update_lookahead, and rollback. Of them, update_lookahead and
rollback are both O(n). But deepcopy is O(n^2) and thus taking up the most time.

So, how do I fix it? Either way, I need to be able to roll things back.
But I had an idea. Rather than copying the whole list, I simply record which things I'm adding and put them on a stack.
Then, when I roll back, I can pop these elements off and add them back. Placing a queen would add, at minimum, 3n
elements, and adding 3n elements is O(n).
My problem is that this shifts the the weight of doing the work for rollback. Right now, each iteration of rollback does
O(1) work reverting our lookahead to a previous version we have stored. This would change it to O(n) where it has to
manually add each element. And rollback is already in the main loop.
But rollback isn't really in the main loop. It really operates in parallel. Rollback is what happens whenever I rollback
With this change, adding is O(n) and removing is also O(n). That seems more balanced.

Note: I collected the set of moves. I need to add it to history and remove it from history, but I'm taking a snack break

Hold on. I think I figured out why my code isn't working. When I roll back, I don't put back any moves I took out from
my tree. But, sometimes I need to. For example, let's say that in row 0, I put down queen 0. Then in row 1, I put down 
queen 2. When doing so, I use up queen 2. Later, it could be that this doesn't work. When we roll everything back, we 
put all the things that queen 2 Assured - like queen 2 in subsequent rows - back. But, we never put queen 2 back, even 
though that when we start row 0 with queen 4, queen 2 in row 1 suddenly should be a valid move again.

Clearly, I need to add queen 2 to my recursive history somewhere. But where? If I put queen 2 in the same place in the
stack as all the things that it Assured, then when we roll back queen 2, we also put it back in the drawing pile.
Instead, I think I need to put queen 2 into the pile that is for the index before queen 2. In this case, we would add it
to the rollback for row 0. So, when we roll back queen 0, queen (0, 2) would become available again. This should work
and I'm happy with it. Let's implement it.

Right now, my algorithm's performance is extremely variable. For some numbers of queens it does great, for others it 
does terribly. I'm tempted to add a random element to even things out, but he might not want that. So, let's stop and
think if I can think of a non-random way to make sure I try better elements first.
'''
