import pytest
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from solver.base import init_bound

def test_init_bound_5x5():
    m, n = 5, 5
    row_list = [[3], [1, 1], [3], [1, 1], [3]]
    col_list = [[3], [1, 1], [3], [1, 1], [3]]
    bound = init_bound(row_list, col_list, m, n)
    
    # Check row 0, block 0 (length 3)
    # Earliest start = 0, Latest end = 5-1 - 0 - 0 = 4
    assert bound[0][0][0] == [0, 4]
    
    # Check row 1, block 0 (length 1)
    # Earliest start = 0, Latest end = 4 - sum([1]) - 1 = 4 - 2 = 2
    assert bound[0][1][0] == [0, 2]
    
    # Check row 1, block 1 (length 1)
    # Earliest start = sum([1]) + 1 = 2, Latest end = 4 - 0 - 0 = 4
    assert bound[0][1][1] == [2, 4]

def test_init_bound_10x10():
    m, n = 10, 10
    row_list = [[1] for _ in range(10)]
    col_list = [[1] for _ in range(10)]
    bound = init_bound(row_list, col_list, m, n)
    
    # Single block length 1 can be anywhere from 0 to 9
    assert bound[0][0][0] == [0, 9]

def test_init_bound_15x15():
    m, n = 15, 15
    row_list = [[5, 3, 2]] + [[] for _ in range(14)]
    col_list = [[] for _ in range(15)]
    bound = init_bound(row_list, col_list, m, n)
    
    # Row 0: [5, 3, 2]
    # Block 0 (length 5) -> lo: 0, hi: 14 - (3+2) - 2 = 7
    assert bound[0][0][0] == [0, 7]
    # Block 1 (length 3) -> lo: 5+1 = 6, hi: 14 - 2 - 1 = 11
    assert bound[0][0][1] == [6, 11]
    # Block 2 (length 2) -> lo: 5+3+2 = 10, hi: 14 - 0 - 0 = 14
    assert bound[0][0][2] == [10, 14]

def test_init_bound_empty():
    m, n = 20, 20
    row_list = [[] for _ in range(20)]
    col_list = [[] for _ in range(20)]
    bound = init_bound(row_list, col_list, m, n)
    
    assert len(bound[0]) == 20
    assert len(bound[0][0]) == 0 # No blocks, so no bounds

def test_init_bound_tight():
    m, n = 5, 5
    row_list = [[1, 1, 1]] + [[]]*4 # lengths: 1, space: 1, 1, space: 1, 1 = total 5
    col_list = [[]]*5
    bound = init_bound(row_list, col_list, m, n)
    
    # Block 0
    assert bound[0][0][0] == [0, 0]
    # Block 1
    assert bound[0][0][1] == [2, 2]
    # Block 2
    assert bound[0][0][2] == [4, 4]

def test_init_bound_20x20_complex():
    m, n = 20, 20
    row_list = [[1, 2, 3, 4, 1]] + [[]]*19
    col_list = [[]]*20
    bound = init_bound(row_list, col_list, m, n)
    
    # sum = 11, spaces = 4, total = 15. Freedom = 20 - 15 = 5.
    # Block 0 -> lo: 0, hi: 19 - (2+3+4+1) - 4 = 19 - 10 - 4 = 5
    assert bound[0][0][0] == [0, 5]
    
    # Block 4 (last) -> lo: 1+2+3+4+4 = 14, hi: 19
    assert bound[0][0][4] == [14, 19]
