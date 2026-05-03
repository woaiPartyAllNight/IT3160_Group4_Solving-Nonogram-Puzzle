import time
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from solver.nonogram_solver import NonogramSolver

def run_benchmark():
    solver = NonogramSolver()
    
    # Very basic 5x5
    row_list_5 = [[5], [1], [5], [1], [5]]
    col_list_5 = [[5], [1, 1, 1], [5], [1, 1, 1], [5]]
    
    start = time.time()
    solver.set_puzzle(5, 5, row_list_5, col_list_5)
    solver.solve(time_limit=5)
    end = time.time()
    print(f"5x5 Puzzle solved in {end - start:.4f} seconds. Solutions found: {len(solver.get_all_solutions())}")
    
    # 10x10 Checkerboard-ish
    row_list_10 = [[1]*5 for _ in range(10)]
    col_list_10 = [[1]*5 for _ in range(10)]
    
    start = time.time()
    solver.set_puzzle(10, 10, row_list_10, col_list_10)
    solver.solve(time_limit=5)
    end = time.time()
    print(f"10x10 Puzzle solved in {end - start:.4f} seconds. Solutions found: {len(solver.get_all_solutions())}")

    # For a full benchmark, actual complex puzzle configurations would be loaded here.

if __name__ == "__main__":
    run_benchmark()
