# =============================================================================
# NONOGRAM SOLVER (Giải câu đố Nonogram)
# Nonogram (hay Picross) là câu đố logic: điền ô đen/trắng vào lưới dựa trên
# các con số gợi ý ở hàng và cột. Mỗi con số chỉ độ dài một đoạn ô đen liên tiếp.
#
# Quy ước giá trị ô:
#   0  = chưa xác định
#   1  = ô đen (filled)
#  -1  = ô trắng / rỗng (blank)
#
# Cấu trúc dữ liệu chính:
#   board[i][j]              : trạng thái ô tại hàng i, cột j
#   bound[0][i][k]           : [start, end] – phạm vi có thể của đoạn đen thứ k ở hàng i
#   bound[1][j][k]           : [start, end] – phạm vi có thể của đoạn đen thứ k ở cột j
#   row_list[i][k]           : độ dài đoạn đen thứ k ở hàng i
#   col_list[j][k]           : độ dài đoạn đen thứ k ở cột j
# =============================================================================

# import time
# start_time = time.time()

import sys
import math
import copy
from pathlib import Path
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Bật chế độ vẽ tương tác (interactive mode) để cập nhật hình ảnh liên tục
plt.ion()

# -----------------------------------------------------------------------------
# HIỂN THỊ BẢNG
# Dùng matplotlib để vẽ bảng dạng heatmap màu hồng nhạt.
# Ô đen (1) sẽ sáng hơn, ô trắng (-1) sẽ tối hơn theo colormap 'pink_r'.
# -----------------------------------------------------------------------------
def display_board(board):
    plt.imshow(board, cmap='pink_r')
    plt.axis('off')
    plt.pause(0.001)  # Tạm dừng ngắn để hình ảnh kịp render

# =============================================================================
# ĐỌC INPUT TỪ FILE
# File input.txt có cấu trúc:
#   Dòng 1  : m n          (số hàng và số cột)
#   m dòng  : gợi ý hàng  (mỗi dòng là dãy số cách nhau bởi dấu cách)
#   n dòng  : gợi ý cột   (tương tự)
# =============================================================================
import copy
input_path = Path(__file__).resolve().parent / 'input.txt'
with input_path.open() as f:
    size   = f.readline()    # đọc kích thước lưới
    values = f.readlines()   # đọc tất cả các dòng gợi ý còn lại

(m, n) = size.strip().split(' ')
m = int(m)   # số hàng
n = int(n)   # số cột

v_rows = values[:m]        # m dòng đầu là gợi ý hàng
v_cols = values[m:m+n]    # n dòng tiếp theo là gợi ý cột

# Chuyển từng dòng văn bản thành list số nguyên
row_list = []
for i in v_rows:
    row_list.append([int(j) for j in i.strip().split()])

col_list = []
for i in v_cols:
    col_list.append([int(j) for j in i.strip().split()])

# Hàm nhập input từ stdin (không dùng mặc định, chỉ để tham khảo)
def inp():
    [m, n] = [int(x) for x in input().split()]
    row_list = [[int(x) for x in input().split()] for i in range(m)]
    col_list = [[int(x) for x in input().split()] for i in range(n)]
    return m, n, row_list, col_list

# m, n, row_list, col_list = inp()  # (đã comment, đang dùng file)

# =============================================================================
# KHỞI TẠO BẢNG VÀ PHẠM VI (BOUND)
# =============================================================================

# Bảng ban đầu: tất cả ô đều chưa xác định (= 0)
board = [[0 for j in range(n)] for i in range(m)]

# bound[0][i][k] = [lo, hi]: đoạn đen thứ k ở hàng i có thể nằm trong [lo, hi]
# bound[1][j][k] = [lo, hi]: đoạn đen thứ k ở cột j có thể nằm trong [lo, hi]
#
# Công thức tính phạm vi ban đầu:
#   lo = (tổng các đoạn trước + số khoảng cách tối thiểu)
#   hi = n (hoặc m) - (tổng các đoạn sau + số khoảng cách tối thiểu)
bound = [
    # Phạm vi hàng: bound[0][i][k]
    [[[
        # lo: nếu là đoạn đầu thì bắt đầu từ 0, ngược lại là sau tổng các đoạn trước
        0 if k == 0 else sum(row_list[i][:k]) + k,
        # hi: nếu là đoạn cuối thì kết thúc ở n, ngược lại trước tổng các đoạn sau
        n if k == len(row_list[i]) else (n-1) - sum(row_list[i][k+1:]) - (len(row_list[i])-k-1)
      ] for k in range(len(row_list[i]))
     ] for i in range(m)
    ],
    # Phạm vi cột: bound[1][j][k]
    [[[
        0 if k == 0 else sum(col_list[j][:k]) + k,
        m if k == len(col_list[j]) else (m-1) - sum(col_list[j][k+1:]) - (len(col_list[j])-k-1)
      ] for k in range(len(col_list[j]))
     ] for j in range(n)
    ]
]

# =============================================================================
# HÀM LOGICAL: SUY LUẬN LOGIC ĐỂ THU HẸP PHẠM VI VÀ TÔ MÀU Ô
# Trả về False nếu phát hiện mâu thuẫn, True nếu ổn định.
# Lặp đi lặp lại cho đến khi không còn thay đổi nào (fixpoint).
# =============================================================================
def logical(board, bound):
    change = True
    while change:
        change = False

        # Cập nhật hình ảnh bảng mỗi vòng lặp
        clear_output(wait=True)
        display_board(board)

        # =====================================================================
        # KIỂM TRA TỪNG HÀNG
        # =====================================================================
        for i in range(m):
            for k in range(len(row_list[i])):
                # Điểm kết thúc của đoạn đen liền trước (hoặc -1 nếu không có)
                previous_end = -1 if k == 0 else bound[0][i][k-1][1]
                # Điểm bắt đầu của đoạn đen liền sau (hoặc n nếu không có)
                forward_start = n if k == len(row_list[i])-1 else bound[0][i][k+1][0]

                # --- RULE 2.1: Các đoạn đen phải xếp thứ tự nghiêm ngặt ---
                # Đoạn k phải bắt đầu sau khi đoạn k-1 kết thúc + 1 ô trắng
                if k > 0:
                    if bound[0][i][k-1][0] + row_list[i][k-1] + 1 > bound[0][i][k][0]:
                        bound[0][i][k][0] = bound[0][i][k-1][0] + row_list[i][k-1] + 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False
                        change = True
                # Đoạn k phải kết thúc trước khi đoạn k+1 bắt đầu - 1 ô trắng
                if k < len(row_list[i])-1:
                    if bound[0][i][k+1][1] - row_list[i][k+1] - 1 < bound[0][i][k][1]:
                        bound[0][i][k][1] = bound[0][i][k+1][1] - row_list[i][k+1] - 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False
                        change = True

                # --- RULE 2.2: Ô ngay ngoài biên phạm vi là ô đen → đẩy biên vào ---
                # Nếu ô trước lo là ô đen, lo phải tăng lên 1
                if bound[0][i][k][0] > 0 and board[i][bound[0][i][k][0]-1] == 1:
                    bound[0][i][k][0] += 1
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                        return False
                    change = True
                # Nếu ô sau hi là ô đen, hi phải giảm xuống 1
                if bound[0][i][k][1] < n-1 and board[i][bound[0][i][k][1]+1] == 1:
                    bound[0][i][k][1] -= 1
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                        return False
                    change = True

                # --- RULE 1.1: Overlapping (giao phần chắc chắn) ---
                # Vùng [hi - len + 1, lo + len - 1] chắc chắn thuộc về đoạn đen này
                # (vì dù đặt đoạn từ trái hay phải, vùng giữa luôn bị phủ)
                for j in range(bound[0][i][k][1] - row_list[i][k] + 1,
                               bound[0][i][k][0] + row_list[i][k]):
                    if (j < bound[0][i][k][0] or j > bound[0][i][k][1]) or board[i][j] == -1:
                        return False
                    elif board[i][j] == 0:
                        board[i][j] = 1
                        change = True

                # --- RULE 3.1: Tô màu giữa 2 ô đen đã biết và thu hẹp phạm vi ---
                # Tìm ô đen đầu tiên (s) và cuối cùng (e) trong vùng được phép
                s = e = n
                for j in range(previous_end+1, forward_start):
                    if board[i][j] == 1:
                        s = j
                        break
                if s != n:
                    for j in range(forward_start-1, previous_end, -1):
                        if board[i][j] == 1:
                            e = j
                            break
                    # Tô tất cả ô giữa s và e là đen
                    for j in range(s+1, e):
                        if board[i][j] == -1:
                            return False
                        elif board[i][j] == 0:
                            board[i][j] = 1
                            change = True
                    # Thu hẹp lo dựa trên vị trí ô đen xa nhất (e)
                    if e - row_list[i][k] + 1 > bound[0][i][k][0]:
                        bound[0][i][k][0] = e - row_list[i][k] + 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False
                        change = True
                    # Thu hẹp hi dựa trên vị trí ô đen gần nhất (s)
                    if s + row_list[i][k] - 1 < bound[0][i][k][1]:
                        bound[0][i][k][1] = s + row_list[i][k] - 1
                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                            return False
                        change = True

                # --- RULE 3.2: Loại bỏ các đoạn trống quá ngắn trong phạm vi ---
                # Quét từ trái: đoạn trống đầu tiên đủ dài → cập nhật lo
                unknown_seg = 0
                for j in range(bound[0][i][k][0], bound[0][i][k][1]+2):
                    if j == bound[0][i][k][1]+1 or board[i][j] == -1:
                        if unknown_seg >= row_list[i][k]:
                            if j - unknown_seg > bound[0][i][k][0]:
                                bound[0][i][k][0] = j - unknown_seg
                                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                    return False
                                change = True
                            break
                        unknown_seg = 0
                        continue
                    unknown_seg += 1
                # Quét từ phải: đoạn trống cuối đủ dài → cập nhật hi
                unknown_seg = 0
                for j in range(bound[0][i][k][1], bound[0][i][k][0]-2, -1):
                    if j == bound[0][i][k][0]-1 or board[i][j] == -1:
                        if unknown_seg >= row_list[i][k]:
                            if j + unknown_seg < bound[0][i][k][1]:
                                bound[0][i][k][1] = j + unknown_seg
                                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                    return False
                                change = True
                            break
                        unknown_seg = 0
                        continue
                    unknown_seg += 1
                # Đánh dấu các đoạn quá ngắn (không thể chứa đoạn đen) là -1
                unknown_seg = 0
                for j in range(bound[0][i][k][0], bound[0][i][k][1]+2):
                    if j == bound[0][i][k][1]+1 or board[i][j] == -1:
                        if unknown_seg < row_list[i][k]:
                            for jj in range(j - unknown_seg, j):
                                if jj > previous_end and jj < forward_start:
                                    if board[i][jj] == 1:
                                        return False
                                    if board[i][jj] == 0:
                                        board[i][jj] = -1
                                        change = True
                        unknown_seg = 0
                        continue
                    unknown_seg += 1

                if bound[0][i][k][0] > previous_end:
                    # --- RULE 3.3.1 (từ trái): Ô đầu phạm vi là đen → hoàn thiện đoạn ---
                    # Nếu lo đang là ô đen thì điền đủ row_list[i][k] ô liên tiếp từ lo
                    if board[i][bound[0][i][k][0]] == 1:
                        for j in range(bound[0][i][k][0]+1, bound[0][i][k][0]+row_list[i][k]):
                            if board[i][j] == -1:
                                return False
                            if board[i][j] == 0:
                                board[i][j] = 1
                                change = True
                        # Thu hẹp hi về lo + len - 1
                        if bound[0][i][k][0] + row_list[i][k] - 1 < bound[0][i][k][1]:
                            bound[0][i][k][1] = bound[0][i][k][0] + row_list[i][k] - 1
                            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                return False
                            change = True
                        # Đẩy lo của đoạn kế tiếp sang phải
                        if k < len(row_list[i])-1:
                            if bound[0][i][k][0] + row_list[i][k] + 1 > bound[0][i][k+1][0]:
                                bound[0][i][k+1][0] = bound[0][i][k][0] + row_list[i][k] + 1
                                if bound[0][i][k+1][1] - bound[0][i][k+1][0] + 1 < row_list[i][k+1]:
                                    return False
                                change = True
                        # Thu hẹp hi của đoạn trước nếu sát biên
                        if k > 0 and bound[0][i][k-1][1] == bound[0][i][k][0]-1:
                            bound[0][i][k-1][1] -= 1
                            if bound[0][i][k-1][1] - bound[0][i][k-1][0] + 1 < row_list[i][k-1]:
                                return False
                            change = True

                    # --- RULE 3.3.2 & 3.3.3 (từ trái): Cập nhật hi theo ô trắng / đoạn đen dài quá ---
                    # Duyệt từ lo đến hi:
                    # - Nếu gặp đoạn đen dài hơn row_list[i][k] → thu hẹp hi
                    # - Nếu gặp ô trắng sau khi đã gặp đen → thu hẹp hi về trước ô trắng
                    first_black = -1
                    seg_len = 0
                    for j in range(bound[0][i][k][0], bound[0][i][k][1]+1):
                        if board[i][j] == 1:
                            seg_len += 1
                            if first_black < 0:
                                first_black = j
                            if j == bound[0][i][k][1] or board[i][j+1] != 1:
                                if j - first_black + 1 > row_list[i][k]:
                                    if j - seg_len - 1 < bound[0][i][k][1]:
                                        bound[0][i][k][1] = j - seg_len - 1
                                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                            return False
                                        change = True
                                    break
                                seg_len = 0
                        elif board[i][j] == -1 and first_black >= 0:
                            if j - 1 < bound[0][i][k][1]:
                                bound[0][i][k][1] = j - 1
                                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                    return False
                                change = True
                            break

                if bound[0][i][k][1] < forward_start:
                    # --- RULE 3.3.1 (từ phải): Ô cuối phạm vi là đen → hoàn thiện đoạn ---
                    if board[i][bound[0][i][k][1]] == 1:
                        for j in range(bound[0][i][k][1]-1, bound[0][i][k][1]-row_list[i][k], -1):
                            if board[i][j] == -1:
                                return False
                            if board[i][j] == 0:
                                board[i][j] = 1
                                change = True
                        if bound[0][i][k][1] - row_list[i][k] + 1 > bound[0][i][k][0]:
                            bound[0][i][k][0] = bound[0][i][k][1] - row_list[i][k] + 1
                            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                return False
                            change = True
                        if k > 0:
                            if bound[0][i][k][1] - row_list[i][k] - 1 < bound[0][i][k-1][1]:
                                bound[0][i][k-1][1] = bound[0][i][k][1] - row_list[i][k] - 1
                                if bound[0][i][k-1][1] - bound[0][i][k-1][0] + 1 < row_list[i][k-1]:
                                    return False
                                change = True
                        if k < len(row_list[i])-1 and bound[0][i][k+1][0] == bound[0][i][k][1]+1:
                            bound[0][i][k+1][0] += 1
                            if bound[0][i][k+1][1] - bound[0][i][k+1][0] + 1 < row_list[i][k+1]:
                                return False
                            change = True

                    # --- RULE 3.3.2 & 3.3.3 (từ phải): Cập nhật lo theo ô trắng / đoạn dài quá ---
                    first_black = n
                    seg_len = 0
                    for j in range(bound[0][i][k][1], bound[0][i][k][0]-1):
                        if board[i][j] == 1:
                            seg_len += 1
                            if first_black > n:
                                first_black = j
                            if j == bound[0][i][k][0] or board[i][j-1] != 1:
                                if first_black - j + 1 > row_list[i][k]:
                                    if j + seg_len + 1 > bound[0][i][k][0]:
                                        bound[0][i][k][0] = j + seg_len + 1
                                        if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                            return False
                                        change = True
                                    break
                        elif board[i][j] == -1 and first_black < n:
                            if j + 1 > bound[0][i][k][0]:
                                bound[0][i][k][0] = j + 1
                                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                                    return False
                                change = True
                            break

                # --- RULE 1.1 (lần 2, sau cập nhật bound): Áp dụng lại overlapping ---
                for j in range(bound[0][i][k][1] - row_list[i][k] + 1,
                               bound[0][i][k][0] + row_list[i][k]):
                    if (j < bound[0][i][k][0] or j > bound[0][i][k][1]) or board[i][j] == -1:
                        return False
                    elif board[i][j] == 0:
                        board[i][j] = 1
                        change = True

            # -----------------------------------------------------------------
            # QUÉT TOÀN HÀNG i (không theo từng đoạn k)
            # fb = chỉ số đoạn đầu tiên còn đang được xét (front bound)
            # lb = chỉ số đoạn cuối cùng đang được xét (last bound)
            # seg = số ô đen liên tiếp trong đoạn hiện tại đang đếm
            # last_blank = vị trí ô trắng gần nhất đã gặp
            # -----------------------------------------------------------------
            fb = 0
            lb = -1
            seg = 0
            last_blank = -1
            for j in range(n):
                # --- RULE 1.3 (đầu phạm vi): Cập nhật lb khi đến đầu phạm vi đoạn mới ---
                # Nếu ô hiện tại là đầu phạm vi của đoạn lb+1:
                #   kiểm tra xem toàn bộ các đoạn từ fb đến lb có độ dài = 1 không
                #   nếu có, ô trước j buộc phải là ô trắng
                if lb < len(row_list[i])-1 and j == bound[0][i][lb+1][0]:
                    if board[i][j] == 1:
                        if j > 0:
                            check1_3 = True
                            for k in range(fb, lb+1):
                                if row_list[i][k] != 1:
                                    check1_3 = False
                                    break
                            if check1_3:
                                if board[i][j-1] == 1:
                                    return False
                                elif board[i][j-1] == 0:
                                    board[i][j-1] = -1
                                    change = True
                    lb += 1

                # Độ dài đoạn đen nhỏ nhất và lớn nhất trong vùng [fb, lb]
                min_run = n if fb <= lb else 0
                max_run = 0
                for k in range(fb, lb+1):
                    min_run = min(min_run, row_list[i][k])
                    max_run = max(max_run, row_list[i][k])

                if board[i][j] == -1:
                    last_blank = j

                if board[i][j] == 1:
                    # --- RULE 1.5.1-3: Ô trắng gần nhất tạo ra tường → gây overlapping ---
                    # Từ ô j, kéo dài tối thiểu min_run ô về phía trước:
                    #   - Nếu trong khoảng [j+1, j+min_run) có ô là 0 → điền đen
                    #   - Nếu gặp ô trắng → ghi nhận blank_ahead
                    blank_ahead = [n, True]
                    for jj in range(j+1, min(n, j+min_run)):
                        if jj < last_blank + min_run:
                            if board[i][jj] == -1:
                                return False
                            elif board[i][jj] == 0:
                                board[i][jj] = 1
                                change = True
                        else:
                            if not blank_ahead[1]:
                                break
                        if board[i][jj] == -1 and blank_ahead[1]:
                            blank_ahead[0] = jj
                            blank_ahead[1] = False
                            if jj >= last_blank + min_run:
                                break
                    # Kéo ngược về phía trái cho đến blank_ahead - min_run
                    for jj in range(j-1, blank_ahead[0]-min_run-1, -1):
                        if board[i][jj] == -1:
                            return False
                        elif board[i][jj] == 0:
                            board[i][jj] = 1
                            change = True

                    seg += 1
                    if j == n-1 or board[i][j+1] != 1:
                        # --- RULE 1.5.4: Nếu tất cả đoạn trong vùng đều bằng seg → đặt ô trắng 2 đầu ---
                        if min_run == max_run and min_run == seg:
                            if j - seg >= 0:
                                if board[i][j-seg] == 1:
                                    return False
                                elif board[i][j-seg] == 0:
                                    board[i][j-seg] = -1
                                    change = True
                            if j + 1 < n:
                                if board[i][j+1] == 1:
                                    return False
                                elif board[i][j+1] == 0:
                                    board[i][j+1] = -1
                                    change = True

                        # --- RULE 2.3: Thu hẹp hi của các đoạn trước đoạn đen hiện tại ---
                        # Đoạn hiện tại dài seg; tìm đoạn nhỏ nhất trong [fb, lb] ≥ seg
                        # → các đoạn trước nó không thể vượt qua j-seg-1
                        for k in range(fb, lb+1):
                            if row_list[i][k] >= seg:
                                for kk in range(fb, k):
                                    if j - seg - 1 < bound[0][i][kk][1]:
                                        bound[0][i][kk][1] = j - seg - 1
                                        if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                                            return False
                                        change = True
                                break
                        # Tương tự, các đoạn sau không thể bắt đầu trước j+2
                        for k in range(lb, fb-1, -1):
                            if row_list[i][k] >= seg:
                                for kk in range(lb, k, -1):
                                    if j + 2 > bound[0][i][kk][0]:
                                        bound[0][i][kk][0] = j + 2
                                        if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                                            return False
                                        change = True
                                break
                        seg = 0

                # --- RULE 1.2+1.4: Nếu điền đen vào j tạo đoạn dài hơn max_run → phải là trắng ---
                if board[i][j] != 1:
                    l = j
                    while l > 0 and board[i][l-1] == 1:
                        l -= 1
                    r = j
                    while r < n-1 and board[i][r+1] == 1:
                        r += 1
                    if r - l + 1 > max_run:
                        if board[i][j] == 1:
                            return False
                        if board[i][j] == 0:
                            board[i][j] = -1
                            change = True

                # --- RULE 1.3 (cuối phạm vi): Cập nhật fb khi đến cuối phạm vi đoạn fb ---
                # Nếu ô hiện tại là ô cuối của phạm vi đoạn fb:
                #   kiểm tra xem toàn bộ các đoạn từ fb đến lb có độ dài = 1 không
                #   nếu có, ô sau j buộc phải là ô trắng
                if fb < len(row_list[i]) and j == bound[0][i][fb][1]:
                    fb += 1
                    if board[i][j] == 1:
                        if j < n-1:
                            check1_3 = True
                            for k in range(fb, lb+1):
                                if row_list[i][k] != 1:
                                    check1_3 = False
                                    break
                            if check1_3:
                                if board[i][j+1] == 1:
                                    return False
                                elif board[i][j+1] == 0:
                                    board[i][j+1] = -1
                                    change = True

        # =====================================================================
        # KIỂM TRA TỪNG CỘT (logic tương tự như hàng, chỉ hoán đổi i ↔ j, m ↔ n)
        # =====================================================================
        for j in range(n):
            for k in range(len(col_list[j])):
                previous_end  = -1 if k == 0 else bound[1][j][k-1][1]
                forward_start = m if k == len(col_list[j])-1 else bound[1][j][k+1][0]

                # --- RULE 2.1 (cột) ---
                if k > 0:
                    if bound[1][j][k-1][0] + col_list[j][k-1] + 1 > bound[1][j][k][0]:
                        bound[1][j][k][0] = bound[1][j][k-1][0] + col_list[j][k-1] + 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False
                        change = True
                if k < len(col_list[j])-1:
                    if bound[1][j][k+1][1] - col_list[j][k+1] - 1 < bound[1][j][k][1]:
                        bound[1][j][k][1] = bound[1][j][k+1][1] - col_list[j][k+1] - 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False
                        change = True

                # --- RULE 2.2 (cột) ---
                if bound[1][j][k][0] > 0 and board[bound[1][j][k][0]-1][j] == 1:
                    bound[1][j][k][0] += 1
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                        return False
                    change = True
                if bound[1][j][k][1] < m-1 and board[bound[1][j][k][1]+1][j] == 1:
                    bound[1][j][k][1] -= 1
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                        return False
                    change = True

                # --- RULE 1.1 (cột) ---
                for i in range(bound[1][j][k][1] - col_list[j][k] + 1,
                               bound[1][j][k][0] + col_list[j][k]):
                    if (i < bound[1][j][k][0] or i > bound[1][j][k][1]) or board[i][j] == -1:
                        return False
                    elif board[i][j] == 0:
                        board[i][j] = 1
                        change = True

                # --- RULE 3.1 (cột) ---
                s = e = m
                for i in range(previous_end+1, forward_start):
                    if board[i][j] == 1:
                        s = i
                        break
                if s != m:
                    for i in range(forward_start-1, previous_end, -1):
                        if board[i][j] == 1:
                            e = i
                            break
                    for i in range(s+1, e):
                        if board[i][j] == -1:
                            print(14)
                            return False
                        elif board[i][j] == 0:
                            board[i][j] = 1
                            change = True
                    if e - col_list[j][k] + 1 > bound[1][j][k][0]:
                        bound[1][j][k][0] = e - col_list[j][k] + 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False
                        change = True
                    if s + col_list[j][k] - 1 < bound[1][j][k][1]:
                        bound[1][j][k][1] = s + col_list[j][k] - 1
                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                            return False
                        change = True

                # --- RULE 3.2 (cột) ---
                unknown_seg = 0
                for i in range(bound[1][j][k][0], bound[1][j][k][1]+2):
                    if i == bound[1][j][k][1]+1 or board[i][j] == -1:
                        if unknown_seg >= col_list[j][k]:
                            if i - unknown_seg > bound[1][j][k][0]:
                                bound[1][j][k][0] = i - unknown_seg
                                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                    return False
                                change = True
                            break
                        unknown_seg = 0
                        continue
                    unknown_seg += 1
                unknown_seg = 0
                for i in range(bound[1][j][k][1], bound[1][j][k][0]-2, -1):
                    if i == bound[1][j][k][0]-1 or board[i][j] == -1:
                        if unknown_seg >= col_list[j][k]:
                            if i + unknown_seg < bound[1][j][k][1]:
                                bound[1][j][k][1] = i + unknown_seg
                                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                    return False
                                change = True
                            break
                        unknown_seg = 0
                        continue
                    unknown_seg += 1
                unknown_seg = 0
                for i in range(bound[1][j][k][0], bound[1][j][k][1]+2):
                    if i == bound[1][j][k][1]+1 or board[i][j] == -1:
                        if unknown_seg < col_list[j][k]:
                            for ii in range(i - unknown_seg, i):
                                if ii > previous_end and ii < forward_start:
                                    if board[ii][j] == 1:
                                        return False
                                    if board[ii][j] == 0:
                                        board[ii][j] = -1
                                        change = True
                        unknown_seg = 0
                        continue
                    unknown_seg += 1

                if bound[1][j][k][0] > previous_end:
                    # --- RULE 3.3.1 (cột, từ trên) ---
                    if board[bound[1][j][k][0]][j] == 1:
                        for i in range(bound[1][j][k][0]+1, bound[1][j][k][0]+col_list[j][k]):
                            if board[i][j] == -1:
                                return False
                            if board[i][j] == 0:
                                board[i][j] = 1
                                change = True
                        if bound[1][j][k][0] + col_list[j][k] - 1 < bound[1][j][k][1]:
                            bound[1][j][k][1] = bound[1][j][k][0] + col_list[j][k] - 1
                            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                return False
                            change = True
                        if k < len(col_list[j])-1:
                            if bound[1][j][k][0] + col_list[j][k] + 1 > bound[1][j][k+1][0]:
                                bound[1][j][k+1][0] = bound[1][j][k][0] + col_list[j][k] + 1
                                if bound[1][j][k+1][1] - bound[1][j][k+1][0] + 1 < col_list[j][k+1]:
                                    return False
                                change = True
                        if k > 0 and bound[1][j][k-1][1] == bound[1][j][k][0]-1:
                            bound[1][j][k-1][1] -= 1
                            if bound[1][j][k-1][1] - bound[1][j][k-1][0] + 1 < col_list[j][k-1]:
                                return False
                            change = True

                    # --- RULE 3.3.2 & 3.3.3 (cột, từ trên) ---
                    first_black = -1
                    seg_len = 0
                    for i in range(bound[1][j][k][0], bound[1][j][k][1]+1):
                        if board[i][j] == 1:
                            seg_len += 1
                            if first_black < 0:
                                first_black = i
                            if i == bound[1][j][k][1] or board[i+1][j] != 1:
                                if i - first_black + 1 > col_list[j][k]:
                                    if i - seg_len - 1 < bound[1][j][k][1]:
                                        bound[1][j][k][1] = i - seg_len - 1
                                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                            return False
                                        change = True
                                    break
                                seg_len = 0
                        elif board[i][j] == -1 and first_black >= 0:
                            if i - 1 < bound[1][j][k][1]:
                                bound[1][j][k][1] = i - 1
                                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                    return False
                                change = True
                            break

                if bound[1][j][k][1] < forward_start:
                    # --- RULE 3.3.1 (cột, từ dưới) ---
                    if board[bound[1][j][k][1]][j] == 1:
                        for i in range(bound[1][j][k][1]-1, bound[1][j][k][1]-col_list[j][k], -1):
                            if board[i][j] == -1:
                                return False
                            if board[i][j] == 0:
                                board[i][j] = 1
                                change = True
                        if bound[1][j][k][1] - col_list[j][k] + 1 > bound[1][j][k][0]:
                            bound[1][j][k][0] = bound[1][j][k][1] - col_list[j][k] + 1
                            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                return False
                            change = True
                        if k > 0:
                            if bound[1][j][k][1] - col_list[j][k] - 1 < bound[1][j][k-1][1]:
                                bound[1][j][k-1][1] = bound[1][j][k][1] - col_list[j][k] - 1
                                if bound[1][j][k-1][1] - bound[1][j][k-1][0] + 1 < col_list[j][k-1]:
                                    return False
                                change = True
                        if k < len(col_list[j])-1 and bound[1][j][k+1][0] == bound[1][j][k][1]+1:
                            bound[1][j][k+1][0] += 1
                            if bound[1][j][k+1][1] - bound[1][j][k+1][0] + 1 < col_list[j][k+1]:
                                return False
                            change = True

                    # --- RULE 3.3.2 & 3.3.3 (cột, từ dưới) ---
                    first_black = m
                    seg_len = 0
                    for i in range(bound[1][j][k][1], bound[1][j][k][0]-1):
                        if board[i][j] == 1:
                            seg_len += 1
                            if first_black > m:
                                first_black = i
                            if i == bound[1][j][k][0] or board[i-1][j] != 1:
                                if first_black - i + 1 > col_list[j][k]:
                                    if i + seg_len + 1 > bound[1][j][k][0]:
                                        bound[1][j][k][0] = i + seg_len + 1
                                        if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                            return False
                                        change = True
                                    break
                        elif board[i][j] == -1 and first_black < m:
                            if i + 1 > bound[1][j][k][0]:
                                bound[1][j][k][0] = i + 1
                                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                                    return False
                                change = True
                            break

                # --- RULE 1.1 (cột, lần 2) ---
                for i in range(bound[1][j][k][1] - col_list[j][k] + 1,
                               bound[1][j][k][0] + col_list[j][k]):
                    if (i < bound[1][j][k][0] or i > bound[1][j][k][1]) or board[i][j] == -1:
                        return False
                    elif board[i][j] == 0:
                        board[i][j] = 1
                        change = True

            # -----------------------------------------------------------------
            # QUÉT TOÀN CỘT j (tương tự quét toàn hàng phía trên)
            # -----------------------------------------------------------------
            fb = 0
            lb = -1
            seg = 0
            last_blank = -1
            for i in range(m):
                # --- RULE 1.3 (cột, đầu phạm vi) ---
                if lb < len(col_list[j])-1 and i == bound[1][j][lb+1][0]:
                    if board[i][j] == 1:
                        if i > 0:
                            check1_3 = True
                            for k in range(fb, lb+1):
                                if col_list[j][k] != 1:
                                    check1_3 = False
                                    break
                            if check1_3:
                                if board[i-1][j] == 1:
                                    return False
                                elif board[i-1][j] == 0:
                                    board[i-1][j] = -1
                                    change = True
                    lb += 1

                min_run = m if lb >= fb else 0
                max_run = 0
                for k in range(fb, lb+1):
                    min_run = min(min_run, col_list[j][k])
                    max_run = max(max_run, col_list[j][k])

                if board[i][j] == -1:
                    last_blank = i

                if board[i][j] == 1:
                    # --- RULE 1.5.1-3 (cột) ---
                    blank_ahead = [m, True]
                    for ii in range(i+1, min(m, i+min_run)):
                        if ii < last_blank + min_run:
                            if board[ii][j] == -1:
                                return False
                            elif board[ii][j] == 0:
                                board[ii][j] = 1
                                change = True
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
                            return False
                        elif board[ii][j] == 0:
                            board[ii][j] = 1
                            change = True

                    seg += 1
                    if i == m-1 or board[i+1][j] != 1:
                        # --- RULE 1.5.4 (cột) ---
                        if min_run == max_run and min_run == seg:
                            if i - seg >= 0:
                                if board[i-seg][j] == 1:
                                    return False
                                elif board[i-seg][j] == 0:
                                    board[i-seg][j] = -1
                                    change = True
                            if i + 1 < m:
                                if board[i+1][j] == 1:
                                    return False
                                elif board[i+1][j] == 0:
                                    board[i+1][j] = -1
                                    change = True

                        # --- RULE 2.3 (cột) ---
                        for k in range(fb, lb+1):
                            if col_list[j][k] >= seg:
                                for kk in range(fb, k):
                                    if i - seg - 1 < bound[1][j][kk][1]:
                                        bound[1][j][kk][1] = i - seg - 1
                                        if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                                            return False
                                        change = True
                                break
                        for k in range(lb, fb-1, -1):
                            if col_list[j][k] >= seg:
                                for kk in range(lb, k, -1):
                                    if i + 2 > bound[1][j][kk][0]:
                                        bound[1][j][kk][0] = i + 2
                                        if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                                            return False
                                        change = True
                                break
                        seg = 0

                # --- RULE 1.2+1.4 (cột) ---
                if board[i][j] != 1:
                    l = i
                    while l > 0 and board[l-1][j] == 1:
                        l -= 1
                    r = i
                    while r < m-1 and board[r+1][j] == 1:
                        r += 1
                    if r - l + 1 > max_run:
                        if board[i][j] == 1:
                            return False
                        if board[i][j] == 0:
                            board[i][j] = -1
                            change = True

                # --- RULE 1.3 (cột, cuối phạm vi) ---
                if fb < len(col_list[j]) and i == bound[1][j][fb][1]:
                    fb += 1
                    if board[i][j] == 1:
                        if i < m-1:
                            check1_3 = True
                            for k in range(fb, lb+1):
                                if col_list[j][k] != 1:
                                    check1_3 = False
                                    break
                            if check1_3:
                                if board[i+1][j] == 1:
                                    return False
                                elif board[i+1][j] == 0:
                                    board[i+1][j] = -1
                                    change = True
    return True


# =============================================================================
# HÀM XUẤT KẾT QUẢ RA STDOUT
# '#' là ô đen, '.' là ô trắng
# =============================================================================
def outp(board):
    for i in range(m):
        for j in range(n):
            if board[i][j] == 1:
                print('#', end='')
            elif board[i][j] == -1:
                print('.', end='')
        print()


# =============================================================================
# HÀM KIỂM TRA BẢNG ĐÃ HOÀN CHỈNH (VERIFY)
# Duyệt từng cột rồi từng hàng, kiểm tra xem chuỗi đoạn đen
# có khớp chính xác với col_list / row_list hay không.
# Trả về True nếu hợp lệ, False nếu sai.
# =============================================================================
def check(board):
    # Kiểm tra từng cột
    for j in range(n):
        i = r = 0
        while i < m:
            if board[i][j] == -1:
                i += 1
            else:
                # Phải còn đoạn cần điền và không vượt quá giới hạn cột
                if r >= len(col_list[j]) or i + col_list[j][r] > m:
                    return False
                # Kiểm tra col_list[j][r] ô liên tiếp từ i đều phải là đen
                for k in range(col_list[j][r]):
                    if board[i+k][j] != 1:
                        return False
                i += col_list[j][r]
                # Ô ngay sau đoạn đen phải là trắng (nếu còn trong bảng)
                if i < m:
                    if board[i][j] != -1:
                        return False
                    i += 1
                r += 1
        if r < len(col_list[j]):
            return False

    # Kiểm tra từng hàng
    for i in range(m):
        j = r = 0
        while j < n:
            if board[i][j] == -1:
                j += 1
            else:
                if r >= len(row_list[i]) or j + row_list[i][r] > n:
                    return False
                for k in range(row_list[i][r]):
                    if board[i][j+k] != 1:
                        return False
                j += row_list[i][r]
                if j < n:
                    if board[i][j] != -1:
                        return False
                    j += 1
                r += 1
        if r < len(row_list[i]):
            return False
    return True


# =============================================================================
# HÀM GHI NHẬN LỜI GIẢI
# Tăng biến đếm sol_count mỗi khi tìm được một lời giải.
# =============================================================================
def solution_found(board):
    global sol_count
    # outp(board)  # Bỏ comment nếu muốn in ra từng lời giải
    sol_count += 1


# =============================================================================
# HÀM BACKTRACK: TÌM KIẾM THEO CHIỀU SÂU CÓ CẮT TỈNH (BACKTRACKING)
# Thuật toán:
#   1. Áp dụng logical() để suy luận và phát hiện mâu thuẫn sớm.
#   2. Nếu còn ô chưa xác định (= 0):
#      - Thử gán -1 (trắng) rồi đệ quy.
#      - Thử gán  1 (đen)  rồi đệ quy.
#      - Return sau khi thử xong ô đầu tiên tìm được.
#   3. Nếu không còn ô nào = 0 → kiểm tra check() → ghi nhận lời giải.
# Dùng deepcopy để mỗi nhánh đệ quy có bản sao riêng của board và bound.
# =============================================================================
def backtrack(x, currboard, currbound):
    # Bước 1: Suy luận logic; nếu phát hiện mâu thuẫn thì cắt tỉnh
    if not logical(currboard, currbound):
        return
    # Bước 2: Tìm ô đầu tiên chưa xác định
    for i in range(m):
        for j in range(n):
            if currboard[i][j] == 0:
                # Thử gán ô trắng (-1)
                newboard = copy.deepcopy(currboard)
                newbound = copy.deepcopy(currbound)
                newboard[i][j] = -1
                backtrack(x+1, newboard, newbound)
                # Thử gán ô đen (1)
                newboard = copy.deepcopy(currboard)
                newbound = copy.deepcopy(currbound)
                newboard[i][j] = 1
                backtrack(x+1, newboard, newbound)
                return  # Chỉ xử lý 1 ô mỗi lần gọi
    # Bước 3: Không còn ô nào = 0, kiểm tra xem bảng có hợp lệ không
    if check(currboard):
        solution_found(currboard)


# =============================================================================
# CHẠY CHƯƠNG TRÌNH
# =============================================================================
sol_count = 0
backtrack(0, board, bound)

if sol_count == 0:
    print('the puzzle has no solution')
else:
    print(f'the puzzle has {sol_count} solution')

# Giữ cửa sổ đồ thị mở cho đến khi người dùng đóng thủ công
plt.ioff()
if plt.get_fignums():
    plt.show()