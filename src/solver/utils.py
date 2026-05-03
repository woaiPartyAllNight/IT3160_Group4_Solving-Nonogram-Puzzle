import pygame
import sys
import copy
from solver.config import INPUT_FILE

class Visualizer:
    def __init__(self):
        self.history = []
        self.m = 0
        self.n = 0
        self.row_list = []
        self.col_list = []
        
        # Pygame configuration
        self.cell_size = 25
        self.margin = 20
        self.clue_area_width = 250   # Increased to accommodate larger clues for 50x50
        self.clue_area_height = 250  # Increased for larger clues
        self.playing = False
        self.step_idx = 0
        self.font = None
        self.screen = None
        self.call_count = 0
        self.skip_interval = 1

    def init_puzzle(self, m, n, row_list, col_list):
        self.m = m
        self.n = n
        self.row_list = row_list
        self.col_list = col_list
        self.history = []
        self.call_count = 0
        
        # Customize step interval based on board size
        total_cells = m * n
        if total_cells <= 100:       # <= 10x10 boards
            self.skip_interval = 1
        elif total_cells < 400:      # 10x10 to <20x20 boards
            self.skip_interval = 2
        elif total_cells <= 625:     # 20x20 to 25x25 boards
            self.skip_interval = 5
        else:                        # > 25x25 boards (e.g., 50x50)
            self.skip_interval = 50

    def record_step(self, board, force_save=False):
        self.call_count += 1
        # Record if force_save is True, or it is the first step, or based on the interval
        if force_save or not self.history or self.call_count % self.skip_interval == 0:
            if not self.history or self.history[-1] != board:
                self.history.append(copy.deepcopy(board))

    def _draw_board(self, board, surface):
        COLOR_EMPTY = (240, 240, 240)    # Light gray for unknown (0)
        COLOR_FILLED = (50, 50, 50)      # Dark gray/black for filled (1)
        COLOR_CROSSED = (200, 50, 50)    # Red for crossed (-1)
        COLOR_GRID = (200, 200, 200)
        COLOR_GRID_THICK = (50, 50, 50)

        start_x = self.margin + self.clue_area_width
        start_y = self.margin + self.clue_area_height

        for i in range(self.m):
            for j in range(self.n):
                rect = pygame.Rect(start_x + j * self.cell_size, start_y + i * self.cell_size, self.cell_size, self.cell_size)
                
                val = board[i][j]
                if val == 1:
                    pygame.draw.rect(surface, COLOR_FILLED, rect)
                else:
                    pygame.draw.rect(surface, COLOR_EMPTY, rect)
                    if val == -1:
                        # Draw X for crossed
                        pad = max(2, self.cell_size // 4)
                        pygame.draw.line(surface, COLOR_CROSSED, (rect.left + pad, rect.top + pad), (rect.right - pad, rect.bottom - pad), 2)
                        pygame.draw.line(surface, COLOR_CROSSED, (rect.left + pad, rect.bottom - pad), (rect.right - pad, rect.top + pad), 2)
                
                # Draw standard thin grid lines
                pygame.draw.rect(surface, COLOR_GRID, rect, 1)

        # Draw thick grid lines every 5 cells
        for i in range(0, self.m + 1, 5):
            y = start_y + i * self.cell_size
            thickness = 2 if i > 0 and i < self.m else 1
            pygame.draw.line(surface, COLOR_GRID_THICK, (start_x, y), (start_x + self.n * self.cell_size, y), thickness)
            
        for j in range(0, self.n + 1, 5):
            x = start_x + j * self.cell_size
            thickness = 2 if j > 0 and j < self.n else 1
            pygame.draw.line(surface, COLOR_GRID_THICK, (x, start_y), (x, start_y + self.m * self.cell_size), thickness)

        # Draw outer boundary
        pygame.draw.rect(surface, COLOR_GRID_THICK, pygame.Rect(start_x, start_y, self.n * self.cell_size, self.m * self.cell_size), 2)

    def _draw_clues(self, surface):
        COLOR_TEXT_ROW = (50, 50, 50)
        COLOR_TEXT_COL = (50, 50, 50)
        
        # Adjust fontsize based on cell spacing
        font_to_use = self.font if self.cell_size >= 15 else pygame.font.SysFont('Arial', max(8, int(self.cell_size * 0.8)))

        start_x = self.margin + self.clue_area_width
        start_y = self.margin + self.clue_area_height

        # Draw row clues on the left
        for i in range(self.m):
            clues = self.row_list[i]
            y = start_y + i * self.cell_size + self.cell_size // 2 - font_to_use.get_height() // 2
            x = start_x - 10
            for clue in reversed(clues):
                text = font_to_use.render(str(clue), True, COLOR_TEXT_ROW)
                x -= text.get_width()
                surface.blit(text, (x, y))
                x -= 6 # Spacing

        # Draw col clues on the top
        for j in range(self.n):
            clues = self.col_list[j]
            x_center = start_x + j * self.cell_size + self.cell_size // 2
            y = start_y - 5
            for clue in reversed(clues):
                text = font_to_use.render(str(clue), True, COLOR_TEXT_COL)
                y -= font_to_use.get_height()
                surface.blit(text, (x_center - text.get_width() // 2, y))
                y -= 2 # Spacing

    def show(self):
        if not self.history:
            print("No history to display.")
            return

        pygame.init()
        self.font = pygame.font.SysFont('Arial', 14)
        
        infoObject = pygame.display.Info()
        max_w = int(infoObject.current_w * 0.9)
        max_h = int(infoObject.current_h * 0.9)

        # Determine clue area sizes based on max clue lengths
        max_row_clues = max((len(r) for r in self.row_list), default=1)
        max_col_clues = max((len(c) for c in self.col_list), default=1)
        
        # Approximate size needed for clues
        self.clue_area_width = max_row_clues * 18 + 10
        self.clue_area_height = max_col_clues * 18 + 10

        avail_grid_w = max_w - (self.margin * 2 + self.clue_area_width)
        avail_grid_h = max_h - (self.margin * 2 + self.clue_area_height + 80)
        
        if self.n > 0 and self.m > 0:
            scale_w = avail_grid_w // self.n
            scale_h = avail_grid_h // self.m
            self.cell_size = max(5, min(30, scale_w, scale_h)) 

        board_w = self.n * self.cell_size
        board_h = self.m * self.cell_size
        
        win_w = self.margin * 2 + self.clue_area_width + board_w
        win_h = self.margin * 2 + self.clue_area_height + board_h + 80

        win_w = max(win_w, 400)
        win_h = max(win_h, 300)

        self.screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption("Step-by-Step Nonogram Solver")

        clock = pygame.time.Clock()
        self.step_idx = 0
        self.playing = False

        # button rects
        btn_y = win_h - 40
        btn_w, btn_h = 80, 30
        play_btn = pygame.Rect(20, btn_y, btn_w, btn_h)
        close_btn = pygame.Rect(110, btn_y, btn_w, btn_h)

        # slider rects
        slider_y = win_h - 60
        slider_w = win_w - 40
        slider_track = pygame.Rect(20, slider_y, slider_w, 5)
        
        dragging = False

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.playing = False
                        self.step_idx = min(self.step_idx + 1, len(self.history) - 1)
                    elif event.key == pygame.K_LEFT:
                        self.playing = False
                        self.step_idx = max(self.step_idx - 1, 0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_btn.collidepoint(event.pos):
                            self.playing = not self.playing
                        elif close_btn.collidepoint(event.pos):
                            running = False
                        else:
                            # Check slider
                            num_steps = len(self.history)
                            if num_steps > 1:
                                handle_x = 20 + int((self.step_idx / (num_steps - 1)) * slider_w)
                                handle_rect = pygame.Rect(handle_x - 10, slider_y - 15, 20, 35)
                                # Larger hit area for track
                                track_hit_rect = pygame.Rect(20, slider_y - 15, slider_w, 35)
                                
                                if handle_rect.collidepoint(event.pos) or track_hit_rect.collidepoint(event.pos):
                                    dragging = True
                                    self.playing = False
                                    rel_x = min(max(event.pos[0] - 20, 0), slider_w)
                                    self.step_idx = int((rel_x / slider_w) * (num_steps - 1))
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        num_steps = len(self.history)
                        if num_steps > 1:
                            rel_x = min(max(event.pos[0] - 20, 0), slider_w)
                            self.step_idx = int((rel_x / slider_w) * (num_steps - 1))

            if self.playing:
                self.step_idx += 1
                if self.step_idx >= len(self.history) - 1:
                    self.step_idx = len(self.history) - 1
                    self.playing = False

            # Draw Base Background
            self.screen.fill((248, 248, 248)) 
            
            # Board & Clues
            current_board = self.history[self.step_idx]
            self._draw_board(current_board, self.screen)
            self._draw_clues(self.screen)

            # Controls
            # Play / Pause Btn
            pygame.draw.rect(self.screen, (220, 220, 220), play_btn)
            pygame.draw.rect(self.screen, (150, 150, 150), play_btn, 1)
            play_text = self.font.render("Pause" if self.playing else "Play", True, (0, 0, 0))
            self.screen.blit(play_text, play_text.get_rect(center=play_btn.center))
            
            # Close Btn
            pygame.draw.rect(self.screen, (220, 220, 220), close_btn)
            pygame.draw.rect(self.screen, (150, 150, 150), close_btn, 1)
            close_text = self.font.render("Close", True, (0, 0, 0))
            self.screen.blit(close_text, close_text.get_rect(center=close_btn.center))

            # Slider Track
            pygame.draw.rect(self.screen, (180, 180, 180), slider_track)
            
            # Slider Handle
            num_steps = len(self.history)
            if num_steps > 1:
                handle_x = 20 + int((self.step_idx / (num_steps - 1)) * slider_w)
                handle_rect = pygame.Rect(handle_x - 5, slider_y - 10, 10, 25)
                pygame.draw.rect(self.screen, (100, 150, 255), handle_rect)
            else:
                # If only 1 step, draw handle at the beginning
                handle_rect = pygame.Rect(20 - 5, slider_y - 10, 10, 25)
                pygame.draw.rect(self.screen, (150, 150, 150), handle_rect)

            # Step Text
            step_text = self.font.render(f"Step {self.step_idx + 1}/{len(self.history)}", True, (50, 50, 50))
            self.screen.blit(step_text, (win_w - step_text.get_width() - 20, btn_y + 5))

            pygame.display.flip()
            
            if self.playing:
                clock.tick(15) # Framerate of playback
            else:
                clock.tick(30)

        pygame.quit()

visualizer = Visualizer()

class InvalidPuzzleError(ValueError):
    pass

def validate_puzzle(m, n, row_list, col_list):
    if m <= 0 or n <= 0:
        raise InvalidPuzzleError("Dimensions must be positive.")

    row_list = [[] if r == [0] else r for r in row_list]
    col_list = [[] if c == [0] else c for c in col_list]

    if len(row_list) != m:
        raise InvalidPuzzleError(f"Expected {m} rows, but got {len(row_list)}.")
    if len(col_list) != n:
        raise InvalidPuzzleError(f"Expected {n} columns, but got {len(col_list)}.")

    for i, r in enumerate(row_list):
        if any(x <= 0 for x in r):
            raise InvalidPuzzleError(f"Non-positive block found in row {i}.")
        if sum(r) + max(0, len(r) - 1) > n:
            raise InvalidPuzzleError(f"Row {i} clues {r} exceed grid width {n}.")

    for j, c in enumerate(col_list):
        if any(x <= 0 for x in c):
            raise InvalidPuzzleError(f"Non-positive block found in column {j}.")
        if sum(c) + max(0, len(c) - 1) > m:
            raise InvalidPuzzleError(f"Column {j} clues {c} exceed grid height {m}.")

    total_row_sum = sum(sum(r) for r in row_list)
    total_col_sum = sum(sum(c) for c in col_list)
    if total_row_sum != total_col_sum:
        raise InvalidPuzzleError(f"Inconsistent puzzle: total row sum ({total_row_sum}) != total column sum ({total_col_sum})")

    return row_list, col_list

def load_puzzle(filename=INPUT_FILE):
    try:
        with open(filename) as f:
            size = f.readline()
            values = f.readlines()
    except FileNotFoundError:
        raise InvalidPuzzleError(f"Puzzle file {filename} not found.")

    try:
        m, n = map(int, size.strip().split())
    except ValueError:
        raise InvalidPuzzleError("Invalid dimensions format.")
    
    if len(values) < m + n:
        raise InvalidPuzzleError(f"Expected {m} rows and {n} columns, but got {len(values)} lines.")
        
    v_rows = values[:m]
    v_cols = values[m:m+n]

    try:
        row_list = [[int(j) for j in i.strip().split()] for i in v_rows]
        col_list = [[int(j) for j in i.strip().split()] for i in v_cols]
    except ValueError:
        raise InvalidPuzzleError("Invalid clue format. Must be integers.")

    row_list, col_list = validate_puzzle(m, n, row_list, col_list)

    return m, n, row_list, col_list

def display_board(board):
    visualizer.record_step(board)

def outp(board):
    for row in board:
        for cell in row:
            print('#' if cell == 1 else '.' if cell == -1 else ' ', end='')
        print()

def check(board, row_list, col_list):
    m, n = len(board), len(board[0])
    # check columns 
    for j in range(n):
        i = r = 0
        while i < m:
            if board[i][j] == -1:
                i += 1
            else:
                if r >= len(col_list[j]) or i + col_list[j][r] > m:
                    return False
                for k in range(col_list[j][r]):
                    if board[i + k][j] != 1:
                        return False
                i += col_list[j][r]
                if i < m:
                    if board[i][j] != -1:
                        return False
                    i += 1
                r += 1
        if r < len(col_list[j]):
            return False
    # check rows 
    for i in range(m):
        j = r = 0
        while j < n:
            if board[i][j] == -1:
                j += 1
            else:
                if r >= len(row_list[i]) or j + row_list[i][r] > n:
                    return False
                for k in range(row_list[i][r]):
                    if board[i][j + k] != 1:
                        return False
                j += row_list[i][r]
                if j < n:
                    if board[i][j] != -1:
                        return False
                    j += 1
                r += 1
        if r < len(row_list[i]):
            return False
    return True