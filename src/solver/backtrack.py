import copy
import time
from solver.utils import check
from solver.logical import logical

class TimeoutException(Exception):
    pass

def get_mrv_cell(board, m, n):
    """Tìm ô trống bị ràng buộc nhiều nhất (heuristic MRV) dựa trên số ô chưa biết."""
    best_cell = None
    min_unknowns = float('inf')
    
    # Tính trước số ô chưa biết trên mỗi hàng và cột
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
        # Khi không còn ô trống nào trên bảng
        if check(currboard, row_list, col_list):
            solutions.append(copy.deepcopy(currboard))
        return

    i, j = cell

    # Thử đặt ô là -1 (dấu X) trước, sau đó là 1 (tô đen)
    newboard = copy.deepcopy(currboard)
    newbound = copy.deepcopy(currbound)
    newboard[i][j] = -1
    backtrack(newboard, newbound, row_list, col_list, m, n, solutions, time_limit, start_time, visualize)

    newboard = copy.deepcopy(currboard)
    newbound = copy.deepcopy(currbound)
    newboard[i][j] = 1
    backtrack(newboard, newbound, row_list, col_list, m, n, solutions, time_limit, start_time, visualize)