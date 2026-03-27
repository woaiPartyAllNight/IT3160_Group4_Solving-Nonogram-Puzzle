#test generator
import random
import sys

m = 4
n = 4
print(m, n)

board = [[1 if random.randint(0,1) else 0 for j in range(n)] for i in range(m)]

row_list = [[] for i in range(m)]
for i in range(m):
    for j in range(n):
        if board[i][j] == 1:
            if j == 0 or board[i][j-1] == 0:
                row_list[i].append(0)
            row_list[i][len(row_list[i])-1] += 1
            if j == n-1 or board[i][j+1] == 0:
                print(row_list[i][len(row_list[i])-1], end=' ')
    print()
            
col_list = [[] for j in range(n)]
for j in range(n):
    for i in range(m):
        if board[i][j] == 1:
            if i == 0 or board[i-1][j] == 0:
                col_list[j].append(0)
            col_list[j][len(col_list[j])-1] += 1
            if i == m-1 or board[i+1][j] == 0:
                print(col_list[j][len(col_list[j])-1], end=' ')
    print()