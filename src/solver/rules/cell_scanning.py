from solver.rules.segment_utils import apply_rule2_3_segment_row, apply_rule2_3_segment_col




# QUY TẮC 1.2 - 1.5 (Quét ô cho hàng)
def apply_rule1_cell_scanning_row(i, board, bound, row_list, m, n):
    changed = False
    fb = 0
    lb = -1         
    seg = 0
    last_blank = -1
    for j in range(n):
        # Quy tắc 1.3: Đánh dấu X trước khối 1 ô ở đầu giới hạn
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
            # Quy tắc 1.5.1-3: Tô đen phần chắc chắn thuộc khối khi gặp ô đen
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
                # Quy tắc 1.5.4: Đặt dấu X hai đầu khi khối đen đạt độ dài tối đa
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
                # Quy tắc 2.3: Thắt chặt giới hạn dựa trên phân đoạn hiện tại
                valid, ch = apply_rule2_3_segment_row(i, j, seg, fb, lb, board, bound, row_list, m, n)
                if not valid:
                    return False, changed
                changed |= ch
                seg = 0

        # Quy tắc 1.2 & 1.4: Đánh dấu X vào ô không thể chứa khối đen nào
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

        # Quy tắc 1.3: Đánh dấu X sau khối 1 ô ở cuối giới hạn
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


# QUY TẮC 1.2 - 1.5 (Quét ô cho cột)
def apply_rule1_cell_scanning_col(j, board, bound, col_list, m, n):
    changed = False
    fb = 0
    lb = -1          
    seg = 0
    last_blank = -1
    for i in range(m):
        # Quy tắc 1.3: Đánh dấu X phía trên khối 1 ô ở đầu giới hạn
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
            # Quy tắc 1.5.1-3: Tô đen phần chắc chắn thuộc khối khi gặp ô đen
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
                # Quy tắc 1.5.4: Đặt dấu X hai đầu khi khối đen đạt độ dài tối đa
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
                # Quy tắc 2.3: Thắt chặt giới hạn dựa trên phân đoạn hiện tại
                valid, ch = apply_rule2_3_segment_col(i, j, seg, fb, lb, board, bound, col_list, m, n)
                if not valid:
                    return False, changed
                changed |= ch
                seg = 0

        # Quy tắc 1.2 & 1.4: Đánh dấu X vào ô không thể chứa khối đen nào
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

        # Quy tắc 1.3: Đánh dấu X phía dưới khối 1 ô ở cuối giới hạn
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