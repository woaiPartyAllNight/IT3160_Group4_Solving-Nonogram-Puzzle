import pytest
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from solver.rules.overlap_inference import apply_rule1_1_block_row
from solver.rules.bound_tightening import apply_rule2_1_block_row
from solver.base import init_board, init_bound

def test_rule1_1_overlap():
    m, n = 1, 5
    row_list = [[4]]
    col_list = [[1], [1], [1], [1], [1]]
    board = init_board(m, n)
    bound = init_bound(row_list, col_list, m, n)
    
    # Block of length 4 in a 5-cell row.
    # Earliest start = 0, latest start = 1. Earliest end = 3, latest end = 4.
    # Overlap is from index 1 to 3.
    valid, changed = apply_rule1_1_block_row(board, bound, 0, 0, row_list, -1, 5, m, n)
    
    assert valid is True
    assert changed is True
    assert board[0] == [0, 1, 1, 1, 0]

def test_rule2_1_bound_tightening():
    m, n = 1, 5
    row_list = [[1, 1]]
    col_list = [[1], [0], [1], [0], [0]]
    board = init_board(m, n)
    bound = init_bound(row_list, col_list, m, n)
    
    # Suppose block 0's bound is forced to start at 2
    bound[0][0][0][0] = 2
    
    valid, changed = apply_rule2_1_block_row(board, bound, 0, 1, row_list, -1, 5, m, n)
    
    # Block 1 should be pushed right by block 0.
    # Earliest start of block 1 becomes 2 + 1 + 1 = 4
    assert valid is True
    assert changed is True
    assert bound[0][0][1][0] == 4
