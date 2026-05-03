"""
NonogramSolver - A solver for nonogram puzzles
"""
import sys
from pathlib import Path

from solver.base import init_board, init_bound
from solver.utils import load_puzzle, validate_puzzle
from solver.backtrack import backtrack, TimeoutException
import time
from solver.config import INPUT_FILE

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
        row_list, col_list = validate_puzzle(m, n, row_list, col_list)
        
        self.m = m
        self.n = n
        self.row_list = row_list
        self.col_list = col_list
        self.board = init_board(m, n)
        self.bound = init_bound(row_list, col_list, m, n)
        self.solutions = []
        
    def set_values(self, col_list, row_list):
        """
        Alias for set_puzzle to match the pipeline invocation from util/nonogram.py
        """
        self.set_puzzle(len(row_list), len(col_list), row_list, col_list)
    
    def solve(self, time_limit=None, visualize=False):
        """
        Solve the nonogram puzzle
        
        Args:
            time_limit: optional time limit in seconds
            visualize: boolean, if True, displays visualizer UI
            
        Returns:
            bool: True if puzzle has been solved (at least 1 solution), False otherwise
        """
        if self.board is None:
            return False
        
        self.solutions = []
        start_time = time.time() if time_limit else None
        
        try:
            backtrack(self.board, self.bound, self.row_list, self.col_list, self.m, self.n, self.solutions, time_limit, start_time, visualize)
        except TimeoutException:
            print("Solver exceeded time limit")
            
        if self.solutions:
            self.board = self.solutions[0]
            
        return len(self.solutions) > 0
    
    def get_solution(self):
        """
        Get the first solution board state
        
        Returns:
            list: 2D list representing the solved nonogram, or None if no solution
        """
        if self.solutions:
            return self.solutions[0]
        return self.board

    def get_all_solutions(self):
        """
        Get all valid solutions found
        
        Returns:
            list: list of 2D lists, each representing a valid solution
        """
        return self.solutions
