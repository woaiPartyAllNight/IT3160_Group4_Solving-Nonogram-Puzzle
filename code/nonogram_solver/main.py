from config import INPUT_FILE
from base import init_board, init_bound
from utils import load_puzzle
from backtrack import backtrack, sol_count

if __name__ == "__main__":
    m, n, row_list, col_list = load_puzzle(INPUT_FILE)
    board = init_board(m, n)
    bound = init_bound(row_list, col_list, m, n)

    backtrack(0, board, bound, row_list, col_list, m, n)