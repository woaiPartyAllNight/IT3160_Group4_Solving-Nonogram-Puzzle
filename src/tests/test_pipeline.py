import pytest
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from solver.nonogram_solver import NonogramSolver

def test_full_pipeline_mock_vision():
    """
    Simulates the end-to-end pipeline:
    1. Vision API provides parsed clues (mocked here).
    2. Solver initializes.
    3. Solver computes result.
    4. Validate output.
    """
    
    # 1. Mock Vision API Output (5x5 cross)
    m, n = 5, 5
    row_clues = [[1], [3], [5], [3], [1]]
    col_clues = [[1], [3], [5], [3], [1]]
    
    # 2. Solver initialization
    solver = NonogramSolver()
    solver.set_puzzle(m, n, row_clues, col_clues)
    
    # 3. Solve
    success = solver.solve(time_limit=5)
    
    # 4. Validate output
    assert success is True
    solutions = solver.get_all_solutions()
    assert len(solutions) >= 1
    
    board = solver.get_solution()
    assert board[2] == [1, 1, 1, 1, 1]  # Middle row full
    assert board[0] == [-1, -1, 1, -1, -1] # Top row center
