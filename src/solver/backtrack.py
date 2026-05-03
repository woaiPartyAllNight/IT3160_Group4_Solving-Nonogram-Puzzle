import copy
import time
from solver.utils import check
from solver.logical import logical

class TimeoutException(Exception):
    pass

def get_mrv_cell(board, m, n):
    """
    Find the most constrained unfilled cell (MRV heuristic).
    We define 'most constrained' as the cell belonging to the row and column
    that have the fewest unknown cells (0s).
    """
    best_cell = None
    min_unknowns = float('inf')
    
    # Precompute unknowns per row and column
    row_unknowns = [sum(1 for j in range(n) if board[i][j] == 0) for i in range(m)]
    col_unknowns = [sum(1 for i in range(m) if board[i][j] == 0) for j in range(n)]
    
    for i in range(m):
        for j in range(n):
            if board[i][j] == 0:
                unknowns = row_unknowns[i] + col_unknowns[j]
                if unknowns < min_unknowns:
                    min_unknowns = unknowns
                    best_cell = (i, j)
                    
    return best_cell

def backtrack(currboard, currbound, row_list, col_list, m, n, solutions, time_limit=None, start_time=None, visualize=False):
    if time_limit and start_time and (time.time() - start_time > time_limit):
        raise TimeoutException("Solver exceeded time limit")

    if not logical(currboard, currbound, row_list, col_list, m, n, visualize=visualize):
        return

    cell = get_mrv_cell(currboard, m, n)
    
    if cell is None:
        # No empty cells left
        if check(currboard, row_list, col_list):
            solutions.append(copy.deepcopy(currboard))
        return

    i, j = cell

    # Try setting to -1 (cross) first, then 1 (fill)
    newboard = copy.deepcopy(currboard)
    newbound = copy.deepcopy(currbound)
    newboard[i][j] = -1
    backtrack(newboard, newbound, row_list, col_list, m, n, solutions, time_limit, start_time, visualize)

    newboard = copy.deepcopy(currboard)
    newbound = copy.deepcopy(currbound)
    newboard[i][j] = 1
    backtrack(newboard, newbound, row_list, col_list, m, n, solutions, time_limit, start_time, visualize)