"""
NonogramSolver - A solver for nonogram puzzles
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from base import init_board, init_bound
from utils import load_puzzle
from backtrack import backtrack, sol_count
from config import INPUT_FILE

class NonogramSolver:
    """
    Solver class for nonogram puzzles
    """
    def __init__(self):
        self.m = 0
        self.n = 0
        self.row_list = []
        self.col_list = []
        self.board = None
        self.bound = None
        self.solutions = []
    
    def set_puzzle(self, m, n, row_list, col_list):
        """
        Set the puzzle parameters
        
        Args:
            m: number of rows
            n: number of columns
            row_list: list of constraints for each row
            col_list: list of constraints for each column
        """
        self.m = m
        self.n = n
        self.row_list = row_list
        self.col_list = col_list
        self.board = init_board(m, n)
        self.bound = init_bound(row_list, col_list, m, n)
        
    def set_values(self, col_list, row_list):
        """
        Alias for set_puzzle to match the pipeline invocation from util/nonogram.py
        """
        self.set_puzzle(len(row_list), len(col_list), row_list, col_list)
    
    def solve(self):
        """
        Solve the nonogram puzzle
        
        Returns:
            bool: True if puzzle has been solved, False otherwise
        """
        if self.board is None:
            return False
        
        backtrack(0, self.board, self.bound, self.row_list, self.col_list, self.m, self.n)
        return True
    
    def get_solution(self):
        """
        Get the current board state (solution)
        
        Returns:
            list: 2D list representing the solved nonogram
        """
        return self.board
