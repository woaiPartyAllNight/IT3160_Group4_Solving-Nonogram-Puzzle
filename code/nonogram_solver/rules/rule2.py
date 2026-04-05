def apply_rule2_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    changed = False
    if k > 0 and bound[0][i][k-1][0] + row_list[i][k-1] + 1 > bound[0][i][k][0]:
        bound[0][i][k][0] = bound[0][i][k-1][0] + row_list[i][k-1] + 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
            return False, changed
        changed = True
    if k < len(row_list[i])-1 and bound[0][i][k+1][1] - row_list[i][k+1] - 1 < bound[0][i][k][1]:
        bound[0][i][k][1] = bound[0][i][k+1][1] - row_list[i][k+1] - 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
            return False, changed
        changed = True
    return True, changed

def apply_rule2_2_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    changed = False
    if bound[0][i][k][0] > 0 and board[i][bound[0][i][k][0]-1] == 1:
        bound[0][i][k][0] += 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: return False, changed
        changed = True
    if bound[0][i][k][1] < n-1 and board[i][bound[0][i][k][1]+1] == 1:
        bound[0][i][k][1] -= 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: return False, changed
        changed = True
    return True, changed

def apply_rule2_3_segment_row(i, j, seg, fb, lb, board, bound, row_list, m, n):
    changed = False
    for k in range(fb, lb+1):
        if row_list[i][k] >= seg:
            for kk in range(fb, k):
                if j - seg - 1 < bound[0][i][kk][1]:
                    bound[0][i][kk][1] = j - seg - 1
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                        return False, changed
                    changed = True
            break
    for k in range(lb, fb-1, -1):
        if row_list[i][k] >= seg:
            for kk in range(lb, k, -1):
                if j + 2 > bound[0][i][kk][0]:
                    bound[0][i][kk][0] = j + 2
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                        return False, changed
                    changed = True
            break
    return True, changed

# ====================== COLUMN VERSIONS ======================
def apply_rule2_1_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    changed = False
    if k > 0 and bound[1][j][k-1][0] + col_list[j][k-1] + 1 > bound[1][j][k][0]:
        bound[1][j][k][0] = bound[1][j][k-1][0] + col_list[j][k-1] + 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False, changed
        changed = True
    if k < len(col_list[j])-1 and bound[1][j][k+1][1] - col_list[j][k+1] - 1 < bound[1][j][k][1]:
        bound[1][j][k][1] = bound[1][j][k+1][1] - col_list[j][k+1] - 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False, changed
        changed = True
    return True, changed

def apply_rule2_2_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    changed = False
    if bound[1][j][k][0] > 0 and board[bound[1][j][k][0]-1][j] == 1:
        bound[1][j][k][0] += 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: return False, changed
        changed = True
    if bound[1][j][k][1] < m-1 and board[bound[1][j][k][1]+1][j] == 1:
        bound[1][j][k][1] -= 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: return False, changed
        changed = True
    return True, changed

def apply_rule2_3_segment_col(i, j, seg, fb, lb, board, bound, col_list, m, n):
    changed = False
    for k in range(fb, lb+1):
        if col_list[j][k] >= seg:
            for kk in range(fb, k):
                if i - seg - 1 < bound[1][j][kk][1]:
                    bound[1][j][kk][1] = i - seg - 1
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                        return False, changed
                    changed = True
            break
    for k in range(lb, fb-1, -1):
        if col_list[j][k] >= seg:
            for kk in range(lb, k, -1):
                if i + 2 > bound[1][j][kk][0]:
                    bound[1][j][kk][0] = i + 2
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                        return False, changed
                    changed = True
            break
    return True, changed