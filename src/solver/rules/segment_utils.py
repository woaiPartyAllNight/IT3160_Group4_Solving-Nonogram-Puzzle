# QUY TẮC 2.3 (Thắt chặt giới hạn)
def apply_rule2_3_segment_row(i, j, seg, fb, lb, board, bound, row_list, m, n):
    changed = False

    # Quét xuôi: thắt chặt giới hạn kết thúc của khối nhỏ hơn
    for k in range(fb, lb+1):
        if row_list[i][k] >= seg:
            for kk in range(fb, k):
                if j - seg - 1 < bound[0][i][kk][1]:
                    bound[0][i][kk][1] = j - seg - 1
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                        return False, changed
                    changed = True
            break
    else:
        return False, changed

    # Quét ngược: thắt chặt giới hạn bắt đầu của khối nhỏ hơn
    for k in range(lb, fb-1, -1):
        if row_list[i][k] >= seg:
            for kk in range(lb, k, -1):
                if j + 2 > bound[0][i][kk][0]:
                    bound[0][i][kk][0] = j + 2
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                        return False, changed
                    changed = True
            break
    else:
        return False, changed

    return True, changed


def apply_rule2_3_segment_col(i, j, seg, fb, lb, board, bound, col_list, m, n):
    changed = False
    
    # Quét xuôi: thắt chặt giới hạn kết thúc của khối nhỏ hơn
    for k in range(fb, lb+1):
        if col_list[j][k] >= seg:
            for kk in range(fb, k):
                if i - seg - 1 < bound[1][j][kk][1]:
                    bound[1][j][kk][1] = i - seg - 1
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                        return False, changed
                    changed = True
            break
    else:
        return False, changed

    # Quét ngược: thắt chặt giới hạn bắt đầu của khối nhỏ hơn
    for k in range(lb, fb-1, -1):
        if col_list[j][k] >= seg:
            for kk in range(lb, k, -1):
                if i + 2 > bound[1][j][kk][0]:
                    bound[1][j][kk][0] = i + 2
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                        return False, changed
                    changed = True
            break
    else:
        return False, changed

    return True, changed