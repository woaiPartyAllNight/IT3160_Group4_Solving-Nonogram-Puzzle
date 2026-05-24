def apply_rule3_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Quy tắc 3.1: Tô đen các ô nằm giữa 2 ô đen đã biết nếu chúng chắc chắn thuộc về cùng một khối."""
    changed = False
    s = e = n
    
    # Tìm ô đen đầu tiên (s) trong khoảng giới hạn cô lập của khối k
    for j in range(previous_end + 1, forward_start):
        if board[i][j] == 1:
            s = j
            break
            
    # Nếu tìm thấy ít nhất một ô đen
    if s != n:
        # Tìm ô đen cuối cùng (e) trong khoảng giới hạn cô lập
        for j in range(forward_start - 1, previous_end, -1):
            if board[i][j] == 1:
                e = j
                break
                
        # Toàn bộ các ô nằm giữa s và e bắt buộc phải được tô đen vì chúng tạo thành một khối liền mạch
        for j in range(s + 1, e):
            if board[i][j] == -1:
                # Mâu thuẫn: Tìm thấy dấu X nằm giữa 2 ô đen của cùng một khối
                return False, changed
            elif board[i][j] == 0:
                board[i][j] = 1
                changed = True
                
        # Cập nhật lại giới hạn sớm nhất (bound[0]) của khối dựa trên ô đen cuối cùng (e)
        if e - row_list[i][k] + 1 > bound[0][i][k][0]:
            bound[0][i][k][0] = e - row_list[i][k] + 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
            
        # Cập nhật lại giới hạn muộn nhất (bound[1]) của khối dựa trên ô đen đầu tiên (s)
        if s + row_list[i][k] - 1 < bound[0][i][k][1]:
            bound[0][i][k][1] = s + row_list[i][k] - 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
            
    return True, changed


def apply_rule3_2_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Quy tắc 3.2: Xử lý các khoảng trống (chưa xác định) quá ngắn, không đủ để chứa khối k."""
    changed = False
    unknown_seg = 0
    
    # Quét xuôi (Từ trái sang phải): Tìm khoảng trống đầu tiên đủ lớn để chứa khối k
    for j in range(bound[0][i][k][0], bound[0][i][k][1] + 2):
        # Nếu chạm vào viền giới hạn hoặc gặp dấu X (-1)
        if j == bound[0][i][k][1] + 1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
                # Ép giới hạn sớm nhất bắt đầu từ vùng có khoảng trống đủ lớn
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
    # Quét ngược (Từ phải sang trái): Tìm khoảng trống cuối cùng đủ lớn để chứa khối k
    for j in range(bound[0][i][k][1], bound[0][i][k][0] - 2, -1):
        if j == bound[0][i][k][0] - 1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
                # Ép giới hạn muộn nhất thu hẹp lại vừa với khoảng trống
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
    # Đánh dấu X (-1) vào các khoảng trống bị cô lập và quá ngắn (không khối nào nằm vừa)
    for j in range(bound[0][i][k][0], bound[0][i][k][1] + 2):
        if j == bound[0][i][k][1] + 1 or board[i][j] == -1:
            if unknown_seg < row_list[i][k]:
                for jj in range(j - unknown_seg, j):
                    # Chỉ đánh dấu X nếu vùng này chắc chắn không thuộc về khối k-1 hoặc k+1
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


def apply_rule3_3_first_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Quy tắc 3.3 (Dành cho Cột - Khối đầu tiên): Mở rộng mảng đen nếu ô đầu tiên của giới hạn đã được tô đen."""
    changed = False

    # 3.3.1: Nếu ô giới hạn trên cùng đã là màu đen, khối k chắc chắn bắt đầu từ đây
    if board[bound[1][j][k][0]][j] == 1:
        # 1. Tô đen toàn bộ phần còn lại của khối từ trên xuống dưới
        for i_idx in range(bound[1][j][k][0] + 1, bound[1][j][k][0] + col_list[j][k]):
            if board[i_idx][j] == -1:
                return False, changed
            if board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
                
        # 2. Thu hẹp giới hạn muộn nhất của khối k
        if bound[1][j][k][0] + col_list[j][k] - 1 < bound[1][j][k][1]:
            bound[1][j][k][1] = bound[1][j][k][0] + col_list[j][k] - 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
            
        # 3. Đánh dấu X (-1) vào ô ngay sau khối để ngăn cách với khối k+1
        end_idx = bound[1][j][k][0] + col_list[j][k]
        if end_idx < m: # Đảm bảo không tràn viền dưới bảng
            if board[end_idx][j] == 1:
                return False, changed # Mâu thuẫn: Khối bị dài hơn quy định
            if board[end_idx][j] == 0:
                board[end_idx][j] = -1
                changed = True

        # 4. Đẩy giới hạn sớm nhất của khối tiếp theo (k+1) lùi xuống
        if k < len(col_list[j]) - 1:
            if end_idx + 1 > bound[1][j][k + 1][0]:
                bound[1][j][k + 1][0] = end_idx + 1
                if bound[1][j][k + 1][1] - bound[1][j][k + 1][0] + 1 < col_list[j][k + 1]:
                    return False, changed
                changed = True
                
        # 5. Cập nhật giới hạn muộn nhất của khối trước đó (k-1)
        if k > 0 and bound[1][j][k - 1][1] == bound[1][j][k][0] - 1:
            bound[1][j][k - 1][1] -= 1
            if bound[1][j][k - 1][1] - bound[1][j][k - 1][0] + 1 < col_list[j][k - 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: Thu hẹp giới hạn khi phát hiện các đoạn đen rời rạc hoặc dấu X
    first_black = -1
    seg_len = 0
    for i_idx in range(bound[1][j][k][0], bound[1][j][k][1] + 1):
        if board[i_idx][j] == 1:
            seg_len += 1
            if first_black < 0:
                first_black = i_idx
            if i_idx == bound[1][j][k][1] or board[i_idx + 1][j] != 1:
                # Nếu đoạn đen hiện tại cộng với khoảng cách từ đầu quá lớn so với kích thước khối
                if i_idx - first_black + 1 > col_list[j][k]:
                    if i_idx - seg_len - 1 < bound[1][j][k][1]:
                        bound[1][j][k][1] = i_idx - seg_len - 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False, changed
                        changed = True
                    break
                seg_len = 0
        elif board[i_idx][j] == -1 and first_black >= 0:
            # Gặp dấu X sau khi đã thấy ô đen, ép giới hạn muộn nhất lại
            if i_idx - 1 < bound[1][j][k][1]:
                bound[1][j][k][1] = i_idx - 1
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                    return False, changed
                changed = True
            break
            
    return True, changed


def apply_rule3_3_last_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Quy tắc 3.3 (Dành cho Hàng - Khối cuối cùng): Hoàn thiện mảng đen nếu ô cuối cùng của giới hạn đã được tô đen."""
    changed = False

    # 3.3.1: Nếu ô giới hạn phải ngoài cùng đã là màu đen, khối k chắc chắn kết thúc tại đây
    if board[i][bound[0][i][k][1]] == 1:
        # 1. Tô đen toàn bộ phần còn lại của khối từ phải sang trái
        for j in range(bound[0][i][k][1] - 1, bound[0][i][k][1] - row_list[i][k], -1):
            if board[i][j] == -1:
                return False, changed
            if board[i][j] == 0:
                board[i][j] = 1
                changed = True
                
        # 2. Cập nhật giới hạn sớm nhất (trái) của khối k
        if bound[0][i][k][1] - row_list[i][k] + 1 > bound[0][i][k][0]:
            bound[0][i][k][0] = bound[0][i][k][1] - row_list[i][k] + 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
            
        # 3. Đánh dấu X (-1) vào ô ngay trước khối để ngăn cách với khối k-1
        start_idx = bound[0][i][k][1] - row_list[i][k]
        if start_idx >= 0: # Đảm bảo không tràn viền trái bảng
            if board[i][start_idx] == 1:
                return False, changed # Mâu thuẫn: Khối dài hơn quy định
            if board[i][start_idx] == 0:
                board[i][start_idx] = -1
                changed = True

        # 4. Đẩy giới hạn muộn nhất của khối phía trước (k-1) lùi sang trái
        if k > 0:
            if start_idx - 1 < bound[0][i][k - 1][1]:
                bound[0][i][k - 1][1] = start_idx - 1
                if bound[0][i][k - 1][1] - bound[0][i][k - 1][0] + 1 < row_list[i][k - 1]:
                    return False, changed
                changed = True
                
        # 5. Cập nhật giới hạn sớm nhất của khối k+1
        if k < len(row_list[i]) - 1 and bound[0][i][k + 1][0] == bound[0][i][k][1] + 1:
            bound[0][i][k + 1][0] += 1
            if bound[0][i][k + 1][1] - bound[0][i][k + 1][0] + 1 < row_list[i][k + 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: Thu hẹp giới hạn đối xứng (quét từ phải sang trái)
    first_black = n
    seg_len = 0
    for j in range(bound[0][i][k][1], bound[0][i][k][0] - 1, -1):
        if board[i][j] == 1:
            seg_len += 1
            if first_black > n - 1:
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
    """Quy tắc 3.1 (Dành cho Cột): Tô đen các ô nằm giữa 2 ô đen đã biết của khối k."""
    changed = False
    s = e = m
    
    # Tìm ô đen đầu tiên (s) từ trên xuống
    for i_idx in range(previous_end + 1, forward_start):
        if board[i_idx][j] == 1:
            s = i_idx
            break
            
    if s != m:
        # Tìm ô đen cuối cùng (e) từ dưới lên
        for i_idx in range(forward_start - 1, previous_end, -1):
            if board[i_idx][j] == 1:
                e = i_idx
                break
                
        # Tô đen khoảng giữa s và e
        for i_idx in range(s + 1, e):
            if board[i_idx][j] == -1:
                return False, changed
            elif board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
                
        # Ép giới hạn sớm nhất (trên cùng)
        if e - col_list[j][k] + 1 > bound[1][j][k][0]:
            bound[1][j][k][0] = e - col_list[j][k] + 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
            
        # Ép giới hạn muộn nhất (dưới cùng)
        if s + col_list[j][k] - 1 < bound[1][j][k][1]:
            bound[1][j][k][1] = s + col_list[j][k] - 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
            
    return True, changed


def apply_rule3_2_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Quy tắc 3.2 (Dành cho Cột): Xử lý các khoảng trống dọc quá ngắn, không đủ chứa khối k."""
    changed = False
    unknown_seg = 0
    
    # Quét xuôi (Từ trên xuống dưới)
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
    # Quét ngược (Từ dưới lên trên)
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
    # Đánh dấu X vào các khoảng trống cô lập không đủ độ dài
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


def apply_rule3_3_first_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n):
    """Quy tắc 3.3 (Dành cho Hàng - Khối đầu tiên): Mở rộng mảng đen nếu ô đầu tiên bên trái đã được tô đen."""
    changed = False

    # 3.3.1: Nếu ô giới hạn bên trái ngoài cùng đã là màu đen
    if board[i][bound[0][i][k][0]] == 1:
        # 1. Tô đen cho đủ khối từ trái sang phải
        for j in range(bound[0][i][k][0] + 1, bound[0][i][k][0] + row_list[i][k]):
            if board[i][j] == -1:
                return False, changed
            if board[i][j] == 0:
                board[i][j] = 1
                changed = True
                
        # 2. Cập nhật lại giới hạn muộn nhất của khối hiện tại
        if bound[0][i][k][0] + row_list[i][k] - 1 < bound[0][i][k][1]:
            bound[0][i][k][1] = bound[0][i][k][0] + row_list[i][k] - 1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False, changed
            changed = True
            
        # 3. Đánh dấu X (-1) vào ô ngay sau khối để ngăn cách
        end_idx = bound[0][i][k][0] + row_list[i][k]
        if end_idx < n: # Đảm bảo không bị tràn viền bảng
            if board[i][end_idx] == 1:
                return False, changed # Mâu thuẫn: Khối bị dài hơn quy định
            if board[i][end_idx] == 0:
                board[i][end_idx] = -1
                changed = True

        # 4. Đẩy giới hạn sớm nhất của khối tiếp theo (k+1) ra xa
        if k < len(row_list[i]) - 1:
            if end_idx + 1 > bound[0][i][k + 1][0]:
                bound[0][i][k + 1][0] = end_idx + 1
                if bound[0][i][k + 1][1] - bound[0][i][k + 1][0] + 1 < row_list[i][k + 1]:
                    return False, changed
                changed = True
                
        # 5. Cập nhật giới hạn muộn nhất của khối trước đó (k-1)
        if k > 0 and bound[0][i][k - 1][1] == bound[0][i][k][0] - 1:
            bound[0][i][k - 1][1] -= 1
            if bound[0][i][k - 1][1] - bound[0][i][k - 1][0] + 1 < row_list[i][k - 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: Thu hẹp giới hạn khi phát hiện đoạn đen rời rạc hoặc dấu X
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


def apply_rule3_3_last_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n):
    """Quy tắc 3.3 (Dành cho Cột - Khối cuối cùng): Hoàn thiện mảng đen nếu ô dưới cùng của giới hạn đã được tô đen."""
    changed = False

    # 3.3.1: Nếu ô giới hạn dưới cùng đã là màu đen
    if board[bound[1][j][k][1]][j] == 1:
        # 1. Tô đen toàn bộ khối từ dưới lên trên
        for i_idx in range(bound[1][j][k][1] - 1, bound[1][j][k][1] - col_list[j][k], -1):
            if board[i_idx][j] == -1:
                return False, changed
            if board[i_idx][j] == 0:
                board[i_idx][j] = 1
                changed = True
                
        # 2. Cập nhật giới hạn trên cùng của khối k
        if bound[1][j][k][1] - col_list[j][k] + 1 > bound[1][j][k][0]:
            bound[1][j][k][0] = bound[1][j][k][1] - col_list[j][k] + 1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False, changed
            changed = True
            
        # 3. Đánh dấu X (-1) vào ô ngay trên khối để ngăn cách
        start_idx = bound[1][j][k][1] - col_list[j][k]
        if start_idx >= 0: # Đảm bảo không tràn viền trên
            if board[start_idx][j] == 1:
                return False, changed # Mâu thuẫn
            if board[start_idx][j] == 0:
                board[start_idx][j] = -1
                changed = True

        # 4. Đẩy giới hạn muộn nhất của khối phía trước (k-1) lên trên
        if k > 0:
            if start_idx - 1 < bound[1][j][k - 1][1]:
                bound[1][j][k - 1][1] = start_idx - 1
                if bound[1][j][k - 1][1] - bound[1][j][k - 1][0] + 1 < col_list[j][k - 1]:
                    return False, changed
                changed = True
                
        # 5. Cập nhật giới hạn sớm nhất của khối k+1
        if k < len(col_list[j]) - 1 and bound[1][j][k + 1][0] == bound[1][j][k][1] + 1:
            bound[1][j][k + 1][0] += 1
            if bound[1][j][k + 1][1] - bound[1][j][k + 1][0] + 1 < col_list[j][k + 1]:
                return False, changed
            changed = True

    # 3.3.2 + 3.3.3: Thu hẹp giới hạn đối xứng (quét từ dưới lên trên)
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