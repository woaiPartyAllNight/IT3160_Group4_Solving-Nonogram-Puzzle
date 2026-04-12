def apply_rule3_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Rule 3.1: Color cells between 2 black cells outside previous/behind range"""
    changed = False
    s = e = n
    for j in range(previous_end + 1, forward_start):
        if board[i][j] == 1:
            s = j
            break
    if s != n:
        for j in range(forward_start - 1, previous_end, -1):
            if board[i][j] == 1:
                e = j
                break
        for j in range(s + 1, e):
            if board[i][j] == -1:
                return False, changed
            elif board[i][j] == 0:
                board[i][j] = 1
                changed = True
        if e - row_list[i][k] + 1 > bound[0][i][k][0]:
            bound[0][i][k][0] = e - row_list[i][k] + 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
        if s + row_list[i][k] - 1 < bound[0][i][k][1]:
            bound[0][i][k][1] = s + row_list[i][k] - 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
    return True, changed


def apply_rule3_2_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Rule 3.2: Handle too short segments in a block range"""
    changed = False
    unknown_seg = 0
    # forward scan
    for j in range(bound[0][i][k][0], bound[0][i][k][1] + 2):
        if j == bound[0][i][k][1] + 1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
                if j - unknown_seg > bound[0][i][k][0]:
                    bound[0][i][k][0] = j - unknown_seg
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                        return False, changed
                    changed = True
                break
            unknown_seg = 0
            continue
        unknown_seg += 1

    unknown_seg = 0
    # backward scan
    for j in range(bound[0][i][k][1], bound[0][i][k][0] - 2, -1):
        if j == bound[0][i][k][0] - 1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
                if j + unknown_seg < bound[0][i][k][1]:
                    bound[0][i][k][1] = j + unknown_seg
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                        return False, changed
                    changed = True
                break
            unknown_seg = 0
            continue
        unknown_seg += 1

    unknown_seg = 0
    # set -1 for too short unknown segments
    for j in range(bound[0][i][k][0], bound[0][i][k][1] + 2):
        if j == bound[0][i][k][1] + 1 or board[i][j] == -1:
            if unknown_seg < row_list[i][k]:
                for jj in range(j - unknown_seg, j):
                    if jj > previous_end and jj < forward_start:
                        if board[i][jj] == 1:
                            return False, changed
                        if board[i][jj] == 0:
                            board[i][jj] = -1
                            changed = True
            unknown_seg = 0
            continue
        unknown_seg += 1
    return True, changed


def apply_rule3_3_first_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Rule 3.3.1 + 3.3.2 + 3.3.3 when first cell of range is considered"""
    changed = False

    # 3.3.1: complete a black run if first cell == 1
    if board[i][bound[0][i][k][0]] == 1:
        for j in range(bound[0][i][k][0] + 1, bound[0][i][k][0] + row_list[i][k]):
            if board[i][j] == -1:
                return False, changed
            if board[i][j] == 0:
                board[i][j] = 1
                changed = True
        if bound[0][i][k][0] + row_list[i][k] - 1 < bound[0][i][k][1]:
            bound[0][i][k][1] = bound[0][i][k][0] + row_list[i][k] - 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
        if k < len(row_list[i]) - 1:
            if bound[0][i][k][0] + row_list[i][k] + 1 > bound[0][i][k + 1][0]:
                bound[0][i][k + 1][0] = bound[0][i][k][0] + row_list[i][k] + 1
                if bound[0][i][k + 1][1] - bound[0][i][k + 1][0] + 1 < row_list[i][k + 1]:
                    return False, changed
                changed = True
        if k > 0 and bound[0][i][k - 1][1] == bound[0][i][k][0] - 1:
            bound[0][i][k - 1][1] -= 1
            if bound[0][i][k - 1][1] - bound[0][i][k - 1][0] + 1 < row_list[i][k - 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: restrict range when including black segments or blank cells
    first_black = -1
    seg_len = 0
    for j in range(bound[0][i][k][0], bound[0][i][k][1] + 1):
        if board[i][j] == 1:
            seg_len += 1
            if first_black < 0:
                first_black = j
            if j == bound[0][i][k][1] or board[i][j + 1] != 1:
                if j - first_black + 1 > row_list[i][k]:
                    if j - seg_len - 1 < bound[0][i][k][1]:
                        bound[0][i][k][1] = j - seg_len - 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False, changed
                        changed = True
                    break
                seg_len = 0
        elif board[i][j] == -1 and first_black >= 0:
            if j - 1 < bound[0][i][k][1]:
                bound[0][i][k][1] = j - 1
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                    return False, changed
                changed = True
            break
    return True, changed


def apply_rule3_3_last_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Rule 3.3.1 + 3.3.2 + 3.3.3 when last cell of range is considered"""
    changed = False

    # 3.3.1: complete a black run if last cell == 1
    if board[i][bound[0][i][k][1]] == 1:
        for j in range(bound[0][i][k][1] - 1, bound[0][i][k][1] - row_list[i][k], -1):
            if board[i][j] == -1:
                return False, changed
            if board[i][j] == 0:
                board[i][j] = 1
                changed = True
        if bound[0][i][k][1] - row_list[i][k] + 1 > bound[0][i][k][0]:
            bound[0][i][k][0] = bound[0][i][k][1] - row_list[i][k] + 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
        if k > 0:
            if bound[0][i][k][1] - row_list[i][k] - 1 < bound[0][i][k - 1][1]:
                bound[0][i][k - 1][1] = bound[0][i][k][1] - row_list[i][k] - 1
                if bound[0][i][k - 1][1] - bound[0][i][k - 1][0] + 1 < row_list[i][k - 1]:
                    return False, changed
                changed = True
        if k < len(row_list[i]) - 1 and bound[0][i][k + 1][0] == bound[0][i][k][1] + 1:
            bound[0][i][k + 1][0] += 1
            if bound[0][i][k + 1][1] - bound[0][i][k + 1][0] + 1 < row_list[i][k + 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: restrict range (symmetric version)
    first_black = n
    seg_len = 0
    for j in range(bound[0][i][k][1], bound[0][i][k][0] - 1, -1):
        if board[i][j] == 1:
            seg_len += 1
            if first_black > n - 1:          # first_black > n-1 nghĩa là chưa tìm thấy
                first_black = j
            if j == bound[0][i][k][0] or board[i][j - 1] != 1:
                if first_black - j + 1 > row_list[i][k]:
                    if j + seg_len + 1 > bound[0][i][k][0]:
                        bound[0][i][k][0] = j + seg_len + 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False, changed
                        changed = True
                    break
                seg_len = 0
        elif board[i][j] == -1 and first_black <= n - 1:
            if j + 1 > bound[0][i][k][0]:
                bound[0][i][k][0] = j + 1
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                    return False, changed
                changed = True
            break
    return True, changed


# ====================== COLUMNS ======================
def apply_rule3_1_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Rule 3.1 for columns (giữ nguyên print(14) debug leftover của code gốc)"""
    changed = False
    s = e = m
    for i_idx in range(previous_end + 1, forward_start):
        if board[i_idx][j] == 1:
            s = i_idx
            break
    if s != m:
        for i_idx in range(forward_start - 1, previous_end, -1):
            if board[i_idx][j] == 1:
                e = i_idx
                break
        for i_idx in range(s + 1, e):
            if board[i_idx][j] == -1:
                print(14)                    # debug leftover từ code gốc
                return False, changed
            elif board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
        if e - col_list[j][k] + 1 > bound[1][j][k][0]:
            bound[1][j][k][0] = e - col_list[j][k] + 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
        if s + col_list[j][k] - 1 < bound[1][j][k][1]:
            bound[1][j][k][1] = s + col_list[j][k] - 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
    return True, changed


def apply_rule3_2_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Rule 3.2 for columns"""
    changed = False
    unknown_seg = 0
    for i_idx in range(bound[1][j][k][0], bound[1][j][k][1] + 2):
        if i_idx == bound[1][j][k][1] + 1 or board[i_idx][j] == -1:
            if unknown_seg >= col_list[j][k]:
                if i_idx - unknown_seg > bound[1][j][k][0]:
                    bound[1][j][k][0] = i_idx - unknown_seg
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                        return False, changed
                    changed = True
                break
            unknown_seg = 0
            continue
        unknown_seg += 1

    unknown_seg = 0
    for i_idx in range(bound[1][j][k][1], bound[1][j][k][0] - 2, -1):
        if i_idx == bound[1][j][k][0] - 1 or board[i_idx][j] == -1:
            if unknown_seg >= col_list[j][k]:
                if i_idx + unknown_seg < bound[1][j][k][1]:
                    bound[1][j][k][1] = i_idx + unknown_seg
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                        return False, changed
                    changed = True
                break
            unknown_seg = 0
            continue
        unknown_seg += 1

    unknown_seg = 0
    for i_idx in range(bound[1][j][k][0], bound[1][j][k][1] + 2):
        if i_idx == bound[1][j][k][1] + 1 or board[i_idx][j] == -1:
            if unknown_seg < col_list[j][k]:
                for ii in range(i_idx - unknown_seg, i_idx):
                    if ii > previous_end and ii < forward_start:
                        if board[ii][j] == 1:
                            return False, changed
                        if board[ii][j] == 0:
                            board[ii][j] = -1
                            changed = True
            unknown_seg = 0
            continue
        unknown_seg += 1
    return True, changed


def apply_rule3_3_first_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Rule 3.3 first block for columns"""
    changed = False

    if board[bound[1][j][k][0]][j] == 1:
        for i_idx in range(bound[1][j][k][0] + 1, bound[1][j][k][0] + col_list[j][k]):
            if board[i_idx][j] == -1:
                return False, changed
            if board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
        if bound[1][j][k][0] + col_list[j][k] - 1 < bound[1][j][k][1]:
            bound[1][j][k][1] = bound[1][j][k][0] + col_list[j][k] - 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
        if k < len(col_list[j]) - 1:
            if bound[1][j][k][0] + col_list[j][k] + 1 > bound[1][j][k + 1][0]:
                bound[1][j][k + 1][0] = bound[1][j][k][0] + col_list[j][k] + 1
                if bound[1][j][k + 1][1] - bound[1][j][k + 1][0] + 1 < col_list[j][k + 1]:
                    return False, changed
                changed = True
        if k > 0 and bound[1][j][k - 1][1] == bound[1][j][k][0] - 1:
            bound[1][j][k - 1][1] -= 1
            if bound[1][j][k - 1][1] - bound[1][j][k - 1][0] + 1 < col_list[j][k - 1]:
                return False, changed
            changed = True

    first_black = -1
    seg_len = 0
    for i_idx in range(bound[1][j][k][0], bound[1][j][k][1] + 1):
        if board[i_idx][j] == 1:
            seg_len += 1
            if first_black < 0:
                first_black = i_idx
            if i_idx == bound[1][j][k][1] or board[i_idx + 1][j] != 1:
                if i_idx - first_black + 1 > col_list[j][k]:
                    if i_idx - seg_len - 1 < bound[1][j][k][1]:
                        bound[1][j][k][1] = i_idx - seg_len - 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False, changed
                        changed = True
                    break
                seg_len = 0
        elif board[i_idx][j] == -1 and first_black >= 0:
            if i_idx - 1 < bound[1][j][k][1]:
                bound[1][j][k][1] = i_idx - 1
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                    return False, changed
                changed = True
            break
    return True, changed


def apply_rule3_3_last_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Rule 3.3 last block for columns"""
    changed = False

    if board[bound[1][j][k][1]][j] == 1:
        for i_idx in range(bound[1][j][k][1] - 1, bound[1][j][k][1] - col_list[j][k], -1):
            if board[i_idx][j] == -1:
                return False, changed
            if board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
        if bound[1][j][k][1] - col_list[j][k] + 1 > bound[1][j][k][0]:
            bound[1][j][k][0] = bound[1][j][k][1] - col_list[j][k] + 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
        if k > 0:
            if bound[1][j][k][1] - col_list[j][k] - 1 < bound[1][j][k - 1][1]:
                bound[1][j][k - 1][1] = bound[1][j][k][1] - col_list[j][k] - 1
                if bound[1][j][k - 1][1] - bound[1][j][k - 1][0] + 1 < col_list[j][k - 1]:
                    return False, changed
                changed = True
        if k < len(col_list[j]) - 1 and bound[1][j][k + 1][0] == bound[1][j][k][1] + 1:
            bound[1][j][k + 1][0] += 1
            if bound[1][j][k + 1][1] - bound[1][j][k + 1][0] + 1 < col_list[j][k + 1]:
                return False, changed
            changed = True

    first_black = m
    seg_len = 0
    for i_idx in range(bound[1][j][k][1], bound[1][j][k][0] - 1, -1):
        if board[i_idx][j] == 1:
            seg_len += 1
            if first_black > m - 1:
                first_black = i_idx
            if i_idx == bound[1][j][k][0] or board[i_idx - 1][j] != 1:
                if first_black - i_idx + 1 > col_list[j][k]:
                    if i_idx + seg_len + 1 > bound[1][j][k][0]:
                        bound[1][j][k][0] = i_idx + seg_len + 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False, changed
                        changed = True
                    break
                seg_len = 0
        elif board[i_idx][j] == -1 and first_black < m:
            if i_idx + 1 > bound[1][j][k][0]:
                bound[1][j][k][0] = i_idx + 1
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                    return False, changed
                changed = True
            break
    return True, changed