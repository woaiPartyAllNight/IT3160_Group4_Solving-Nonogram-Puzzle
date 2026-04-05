import copy
from utils import check
from logical import logical

sol_count = 0

def solution_found(board):
    global sol_count
    sol_count += 1

def backtrack(x, currboard, currbound, row_list, col_list, m, n):
    if not logical(currboard, currbound, row_list, col_list, m, n):
        return
    for i in range(m):
        for j in range(n):
            if currboard[i][j] == 0:
                newboard = copy.deepcopy(currboard)
                newbound = copy.deepcopy(currbound)
                newboard[i][j] = -1
                backtrack(x+1, newboard, newbound, row_list, col_list, m, n)
                newboard = copy.deepcopy(currboard)
                newbound = copy.deepcopy(currbound)
                newboard[i][j] = 1
                backtrack(x+1, newboard, newbound, row_list, col_list, m, n)
                return
    if check(currboard, row_list, col_list):
        solution_found(currboard)