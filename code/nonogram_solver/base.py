def init_board(m, n):
    return [[0 for _ in range(n)] for _ in range(m)]

def init_bound(row_list, col_list, m, n):
    bound = [[[[
               0 if k == 0 else sum(row_list[i][:k]) + k,
               n if k == len(row_list[i]) else (n-1) - sum(row_list[i][k+1:]) - (len(row_list[i])-k-1)
               ] for k in range(len(row_list[i]))
              ] for i in range(m)
             ],
             [[[
               0 if k == 0 else sum(col_list[j][:k]) + k,
               m if k == len(col_list[j]) else (m-1) - sum(col_list[j][k+1:]) - (len(col_list[j])-k-1)
               ] for k in range(len(col_list[j]))
              ] for j in range(n)
             ]
            ]
    return bound