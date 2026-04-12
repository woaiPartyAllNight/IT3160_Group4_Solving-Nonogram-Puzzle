from rules.rule2 import apply_rule2_3_segment_row, apply_rule2_3_segment_col

# RULE 1.1 (Overlapping fill) 
def apply_rule1_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Rule 1.1: overlapping - fill black cells in the middle of block range"""
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
    """Rule 1.1 for columns"""
    changed = False
    for i_idx in range(bound[1][j][k][1] - col_list[j][k] + 1,
                       bound[1][j][k][0] + col_list[j][k]):
        if (i_idx < bound[1][j][k][0] or i_idx > bound[1][j][k][1]) or board[i_idx][j] == -1:
            return False, changed
        elif board[i_idx][j] == 0:
            board[i_idx][j] = 1
            changed = True
    return True, changed


# RULE 1.2 + 1.3 + 1.4 + 1.5 (Cell scanning) 
def apply_rule1_cell_scanning_row(i, board, bound, row_list, m, n):
    changed = False
    fb = 0
    lb = -1         
    seg = 0
    last_blank = -1
    for j in range(n):
        # rule 1.3: all current black runs have size 1 at the start of a block range
        if lb < len(row_list[i])-1 and j == bound[0][i][lb+1][0]:
            if board[i][j] == 1 and j > 0:
                if all(row_list[i][k] == 1 for k in range(fb, lb+1)):
                    if board[i][j-1] == 1:
                        return False, changed
                    if board[i][j-1] == 0:
                        board[i][j-1] = -1
                        changed = True
            lb += 1

        min_run = n if fb <= lb else 0
        max_run = 0
        for k in range(fb, lb+1):
            min_run = min(min_run, row_list[i][k])
            max_run = max(max_run, row_list[i][k])

        if board[i][j] == -1:
            last_blank = j

        if board[i][j] == 1:
            # rule 1.5.1-3
            blank_ahead = [n, True]
            for jj in range(j+1, min(n, j+min_run)):
                if jj < last_blank + min_run:
                    if board[i][jj] == -1:
                        return False, changed
                    if board[i][jj] == 0:
                        board[i][jj] = 1
                        changed = True
                else:
                    if not blank_ahead[1]:
                        break
                if board[i][jj] == -1 and blank_ahead[1]:
                    blank_ahead[0] = jj
                    blank_ahead[1] = False
                    if jj >= last_blank + min_run:
                        break
            for jj in range(j-1, blank_ahead[0]-min_run-1, -1):
                if board[i][jj] == -1:
                    return False, changed
                if board[i][jj] == 0:
                    board[i][jj] = 1
                    changed = True

            seg += 1
            if j == n-1 or board[i][j+1] != 1:
                # rule 1.5.4
                if min_run == max_run == seg:
                    if j-seg >= 0:
                        if board[i][j-seg] == 1:
                            return False, changed
                        if board[i][j-seg] == 0:
                            board[i][j-seg] = -1
                            changed = True
                    if j+1 < n:
                        if board[i][j+1] == 1:
                            return False, changed
                        if board[i][j+1] == 0:
                            board[i][j+1] = -1
                            changed = True
                # rule 2.3
                valid, ch = apply_rule2_3_segment_row(i, j, seg, fb, lb, board, bound, row_list, m, n)
                if not valid:
                    return False, changed
                changed |= ch
                seg = 0

        # rule 1.2 + 1.4
        if board[i][j] != 1:
            l = j
            while l > 0 and board[i][l-1] == 1:
                l -= 1
            r = j
            while r < n-1 and board[i][r+1] == 1:
                r += 1
            if r - l + 1 > max_run:
                if board[i][j] == 0:
                    board[i][j] = -1
                    changed = True

        # rule 1.3: all current black runs have size 1 at the end of a block range
        if fb < len(row_list[i]) and j == bound[0][i][fb][1]:
            fb += 1
            if board[i][j] == 1 and j < n-1:
                if all(row_list[i][k] == 1 for k in range(fb, lb+1)):
                    if board[i][j+1] == 1:
                        return False, changed
                    if board[i][j+1] == 0:
                        board[i][j+1] = -1
                        changed = True
    return True, changed


def apply_rule1_cell_scanning_col(j, board, bound, col_list, m, n):
    changed = False
    fb = 0
    lb = -1          
    seg = 0
    last_blank = -1
    for i in range(m):
        if lb < len(col_list[j])-1 and i == bound[1][j][lb+1][0]:
            if board[i][j] == 1 and i > 0:
                if all(col_list[j][k] == 1 for k in range(fb, lb+1)):
                    if board[i-1][j] == 1:
                        return False, changed
                    if board[i-1][j] == 0:
                        board[i-1][j] = -1
                        changed = True
            lb += 1

        min_run = m if lb >= fb else 0
        max_run = 0
        for k in range(fb, lb+1):
            min_run = min(min_run, col_list[j][k])
            max_run = max(max_run, col_list[j][k])

        if board[i][j] == -1:
            last_blank = i

        if board[i][j] == 1:
            blank_ahead = [m, True]
            for ii in range(i+1, min(m, i+min_run)):
                if ii < last_blank + min_run:
                    if board[ii][j] == -1:
                        return False, changed
                    if board[ii][j] == 0:
                        board[ii][j] = 1
                        changed = True
                else:
                    if not blank_ahead[1]:
                        break
                if board[ii][j] == -1 and blank_ahead[1]:
                    blank_ahead[0] = ii
                    blank_ahead[1] = False
                    if ii >= last_blank + min_run:
                        break
            for ii in range(i-1, blank_ahead[0]-min_run-1, -1):
                if board[ii][j] == -1:
                    return False, changed
                if board[ii][j] == 0:
                    board[ii][j] = 1
                    changed = True

            seg += 1
            if i == m-1 or board[i+1][j] != 1:
                if min_run == max_run == seg:
                    if i-seg >= 0:
                        if board[i-seg][j] == 1:
                            return False, changed
                        if board[i-seg][j] == 0:
                            board[i-seg][j] = -1
                            changed = True
                    if i+1 < m:
                        if board[i+1][j] == 1:
                            return False, changed
                        if board[i+1][j] == 0:
                            board[i+1][j] = -1
                            changed = True
                valid, ch = apply_rule2_3_segment_col(i, j, seg, fb, lb, board, bound, col_list, m, n)
                if not valid:
                    return False, changed
                changed |= ch
                seg = 0

        if board[i][j] != 1:
            l = i
            while l > 0 and board[l-1][j] == 1:
                l -= 1
            r = i
            while r < m-1 and board[r+1][j] == 1:
                r += 1
            if r - l + 1 > max_run:
                if board[i][j] == 0:
                    board[i][j] = -1
                    changed = True

        if fb < len(col_list[j]) and i == bound[1][j][fb][1]:
            fb += 1
            if board[i][j] == 1 and i < m-1:
                if all(col_list[j][k] == 1 for k in range(fb, lb+1)):
                    if board[i+1][j] == 1:
                        return False, changed
                    if board[i+1][j] == 0:
                        board[i+1][j] = -1
                        changed = True
    return True, changed