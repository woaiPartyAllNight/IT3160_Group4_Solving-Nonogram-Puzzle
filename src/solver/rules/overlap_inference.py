# QUY TẮC 1.1 (Xử lý chồng lấp khối)
def apply_rule1_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Quy tắc 1.1: Xử lý chồng lấp - Tô đen các ô đen ở giữa phạm vi khối"""
    changed = False
    for j in range(bound[0][i][k][1] - row_list[i][k] + 1,
                   bound[0][i][k][0] + row_list[i][k]):
        if (j < bound[0][i][k][0] or j > bound[0][i][k][1]) or board[i][j] == -1:
            return False, changed
        elif board[i][j] == 0:
            board[i][j] = 1
            changed = True
    return True, changed

def apply_rule1_1_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Quy tắc 1.1 cho cột"""
    changed = False
    for i_idx in range(bound[1][j][k][1] - col_list[j][k] + 1,
                       bound[1][j][k][0] + col_list[j][k]):
        if (i_idx < bound[1][j][k][0] or i_idx > bound[1][j][k][1]) or board[i_idx][j] == -1:
            return False, changed
        elif board[i_idx][j] == 0:
            board[i_idx][j] = 1
            changed = True
    return True, changed
