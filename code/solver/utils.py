from config import INPUT_FILE
import matplotlib.pyplot as plt
from IPython.display import clear_output

def load_puzzle(filename=INPUT_FILE):
    with open(filename) as f:
        size = f.readline()
        values = f.readlines()
    m, n = map(int, size.strip().split())
    v_rows = values[:m]
    v_cols = values[m:m+n]
    row_list = [[int(j) for j in i.strip().split()] for i in v_rows]
    col_list = [[int(j) for j in i.strip().split()] for i in v_cols]
    return m, n, row_list, col_list

def display_board(board):
    plt.imshow(board, cmap='pink_r')
    plt.axis('off')
    plt.show()

def outp(board):
    for row in board:
        for cell in row:
            print('#' if cell == 1 else '.' if cell == -1 else ' ', end='')
        print()

def check(board, row_list, col_list):
    m, n = len(board), len(board[0])
    # check columns 
    for j in range(n):
        i = r = 0
        while i < m:
            if board[i][j] == -1:
                i += 1
            else:
                if r >= len(col_list[j]) or i + col_list[j][r] > m:
                    return False
                for k in range(col_list[j][r]):
                    if board[i + k][j] != 1:
                        return False
                i += col_list[j][r]
                if i < m:
                    if board[i][j] != -1:
                        return False
                    i += 1
                r += 1
        if r < len(col_list[j]):
            return False
    # check rows 
    for i in range(m):
        j = r = 0
        while j < n:
            if board[i][j] == -1:
                j += 1
            else:
                if r >= len(row_list[i]) or j + row_list[i][r] > n:
                    return False
                for k in range(row_list[i][r]):
                    if board[i][j + k] != 1:
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