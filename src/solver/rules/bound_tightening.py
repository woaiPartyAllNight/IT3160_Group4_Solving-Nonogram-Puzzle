def apply_rule2_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    changed = False
    # Cập nhật giới hạn bắt đầu sớm nhất dựa trên khối k-1 phía trước
    if k > 0 and bound[0][i][k-1][0] + row_list[i][k-1] + 1 > bound[0][i][k][0]:
        bound[0][i][k][0] = bound[0][i][k-1][0] + row_list[i][k-1] + 1
        # Trả về False nếu khoảng trống còn lại nhỏ hơn kích thước khối k
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
            return False, changed
        changed = True
    # Cập nhật giới hạn kết thúc muộn nhất dựa trên khối k+1 phía sau
    if k < len(row_list[i])-1 and bound[0][i][k+1][1] - row_list[i][k+1] - 1 < bound[0][i][k][1]:
        bound[0][i][k][1] = bound[0][i][k+1][1] - row_list[i][k+1] - 1
        # Trả về False nếu khoảng trống còn lại nhỏ hơn kích thước khối k
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
            return False, changed
        changed = True
    return True, changed

def apply_rule2_2_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    changed = False
    
    # 1. Kiểm tra ô NGAY TRƯỚC giới hạn bắt đầu sớm nhất
    if bound[0][i][k][0] > 0 and board[i][bound[0][i][k][0]-1] == 1:
        bound[0][i][k][0] += 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: 
            return False, changed
        changed = True

    # 2. Kiểm tra ô NGAY SAU khi đặt khối ở vị trí sớm nhất
    earliest_end = bound[0][i][k][0] + row_list[i][k] - 1
    if earliest_end + 1 < n and board[i][earliest_end + 1] == 1:
        bound[0][i][k][0] += 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: 
            return False, changed
        changed = True

    # 3. Kiểm tra ô NGAY SAU giới hạn kết thúc muộn nhất
    if bound[0][i][k][1] < n-1 and board[i][bound[0][i][k][1]+1] == 1:
        bound[0][i][k][1] -= 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: 
            return False, changed
        changed = True

    # 4. Kiểm tra ô NGAY TRƯỚC khi đặt khối ở vị trí muộn nhất
    latest_start = bound[0][i][k][1] - row_list[i][k] + 1
    if latest_start - 1 >= 0 and board[i][latest_start - 1] == 1:
        bound[0][i][k][1] -= 1
        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]: 
            return False, changed
        changed = True

    return True, changed


# ====================== (COLUMN VERSIONS) ======================
def apply_rule2_1_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    changed = False
    # Cập nhật giới hạn bắt đầu sớm nhất dựa trên khối k-1 phía trên
    if k > 0 and bound[1][j][k-1][0] + col_list[j][k-1] + 1 > bound[1][j][k][0]:
        bound[1][j][k][0] = bound[1][j][k-1][0] + col_list[j][k-1] + 1
        # Trả về False nếu khoảng trống còn lại nhỏ hơn kích thước khối k
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False, changed
        changed = True
    # Cập nhật giới hạn kết thúc muộn nhất dựa trên khối k+1 phía dưới
    if k < len(col_list[j])-1 and bound[1][j][k+1][1] - col_list[j][k+1] - 1 < bound[1][j][k][1]:
        bound[1][j][k][1] = bound[1][j][k+1][1] - col_list[j][k+1] - 1
        # Trả về False nếu khoảng trống còn lại nhỏ hơn kích thước khối k
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False, changed
        changed = True
    return True, changed

def apply_rule2_2_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    changed = False
    
    # 1. Kiểm tra ô NGAY TRÊN giới hạn bắt đầu sớm nhất
    if bound[1][j][k][0] > 0 and board[bound[1][j][k][0]-1][j] == 1:
        bound[1][j][k][0] += 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: 
            return False, changed
        changed = True

    # 2. Kiểm tra ô NGAY DƯỚI khi đặt khối ở vị trí sớm nhất
    earliest_end = bound[1][j][k][0] + col_list[j][k] - 1
    if earliest_end + 1 < m and board[earliest_end + 1][j] == 1:
        bound[1][j][k][0] += 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: 
            return False, changed
        changed = True

    # 3. Kiểm tra ô NGAY DƯỚI giới hạn kết thúc muộn nhất
    if bound[1][j][k][1] < m-1 and board[bound[1][j][k][1]+1][j] == 1:
        bound[1][j][k][1] -= 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: 
            return False, changed
        changed = True

    # 4. Kiểm tra ô NGAY TRÊN khi đặt khối ở vị trí muộn nhất
    latest_start = bound[1][j][k][1] - col_list[j][k] + 1
    if latest_start - 1 >= 0 and board[latest_start - 1][j] == 1:
        bound[1][j][k][1] -= 1
        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]: 
            return False, changed
        changed = True

    return True, changed

