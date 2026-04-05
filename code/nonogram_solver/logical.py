from rules.rule1 import (
    apply_rule1_1_block_row,
    apply_rule1_1_block_col,
    apply_rule1_cell_scanning_row,
    apply_rule1_cell_scanning_col
)
from rules.rule2 import (
    apply_rule2_1_block_row,
    apply_rule2_2_block_row,
    apply_rule2_1_block_col,
    apply_rule2_2_block_col
)
from rules.rule3 import (
    apply_rule3_1_block_row,
    apply_rule3_2_block_row,
    apply_rule3_3_first_block_row,
    apply_rule3_3_last_block_row,
    apply_rule3_1_block_col,
    apply_rule3_2_block_col,
    apply_rule3_3_first_block_col,
    apply_rule3_3_last_block_col
)
from utils import display_board
from IPython.display import clear_output


def logical(board, bound, row_list, col_list, m, n):
    change = True
    while change:
        change = False
        
        # display
        clear_output(wait=True)
        display_board(board)

        # ==================== ROWS ====================
        for i in range(m):
            for k in range(len(row_list[i])):
                previous_end = -1 if k == 0 else bound[0][i][k-1][1]
                forward_start = n if k == len(row_list[i])-1 else bound[0][i][k+1][0]

                # Các rule block (2.1, 2.2, 1.1, 3.1, 3.2)
                for func in [apply_rule2_1_block_row, apply_rule2_2_block_row,
                             apply_rule1_1_block_row, apply_rule3_1_block_row,
                             apply_rule3_2_block_row]:
                    valid, ch = func(board, bound, i, k, row_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 3.3 first block
                if bound[0][i][k][0] > previous_end:
                    valid, ch = apply_rule3_3_first_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 3.3 last block
                if bound[0][i][k][1] < forward_start:
                    valid, ch = apply_rule3_3_last_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 1.1 
                valid, ch = apply_rule1_1_block_row(board, bound, i, k, row_list, previous_end, forward_start, m, n)
                if not valid:
                    return False
                change |= ch

            # Cell scanning cho row
            valid, ch = apply_rule1_cell_scanning_row(i, board, bound, row_list, m, n)
            if not valid:
                return False
            change |= ch

        # ==================== COLUMNS ====================
        for j in range(n):
            for k in range(len(col_list[j])):
                previous_end = -1 if k == 0 else bound[1][j][k-1][1]
                forward_start = m if k == len(col_list[j])-1 else bound[1][j][k+1][0]

                # Các rule block (2.1, 2.2, 1.1, 3.1, 3.2)
                for func in [apply_rule2_1_block_col, apply_rule2_2_block_col,
                             apply_rule1_1_block_col, apply_rule3_1_block_col,
                             apply_rule3_2_block_col]:
                    valid, ch = func(board, bound, j, k, col_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 3.3 first block
                if bound[1][j][k][0] > previous_end:
                    valid, ch = apply_rule3_3_first_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 3.3 last block
                if bound[1][j][k][1] < forward_start:
                    valid, ch = apply_rule3_3_last_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n)
                    if not valid:
                        return False
                    change |= ch

                # Rule 1.1 
                valid, ch = apply_rule1_1_block_col(board, bound, j, k, col_list, previous_end, forward_start, m, n)
                if not valid:
                    return False
                change |= ch

            # Cell scanning cho column
            valid, ch = apply_rule1_cell_scanning_col(j, board, bound, col_list, m, n)
            if not valid:
                return False
            change |= ch

    return True
