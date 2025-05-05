from collections import Counter


class QueensSolver:
  """
  A class used to solve the LinkedIn Queens puzzle using a recursive backtracking algorithm.
  
  The algorithm prioritizes placing queens in the most constrained positions (row, column, or color)
  to efficiently find a solution where:
  - Each row contains exactly one queen
  - Each column contains exactly one queen 
  - Each color contains exactly one queen
  - No queen can be adjacent to another queen (including diagonally)
  """

  def __init__(self, initial_board: list[list[int]], queens: list[tuple[int, int]] = []):
    """
    Initialize the Queens Solver with an initial board state.
    
    Args:
        initial_board: 2D list representing the board with color values
        queens: List of (row, col) coordinates of any pre-placed queens
    """
    self.board = initial_board
    self.n = len(initial_board)
    self.queens: list[tuple[int, int]] = []

    # Track which rows, columns, and colors already have queens
    self.rows_solved: list[bool] = [False] * self.n
    self.cols_solved: list[bool] = [False] * self.n
    self.colors_solved: list[bool] = [False] * self.n

    # Place any pre-existing queens on the board
    for r, c in queens:
      print(f'Placing queen at {r}, {c}')
      self.place_queen(r, c) 
  
  def print_board(self):
    """
    Print the current state of the board with queens marked with an asterisk.
    Used for debugging.
    """
    for r in range(self.n):
      for c in range(self.n):
        if (r, c) in self.queens:
          print(f'{self.board[r][c]}*', end=' ')
        else:
          print(f"{self.board[r][c]} ", end=' ')
      print()

  def place_queen(self, r: int, c: int):
    """
    Place a queen at the specified position and update constraints.
    
    Args:
        r: Row index
        c: Column index
    """
    self.queens.append((r, c))
    self.colors_solved[self.board[r][c]] = True
    self.rows_solved[r] = True
    self.cols_solved[c] = True


  def remove_queen(self, r: int, c: int):
    """
    Remove a queen from the specified position and update constraints.
    Used during backtracking.
    
    Args:
        r: Row index
        c: Column index
    """
    self.queens.remove((r, c))
    self.colors_solved[self.board[r][c]] = False
    self.rows_solved[r] = False
    self.cols_solved[c] = False

  def is_near_queen(self, r: int, c: int):
    """
    Check if a position is adjacent to any existing queen (including diagonally).
    
    Args:
        r: Row index
        c: Column index
        
    Returns:
        bool: True if position is adjacent to any queen, False otherwise
    """
    for qr, qc in self.queens:
      if abs(qr - r) <= 1 and abs(qc - c) <= 1:
        return True
    return False

  def solve(self) -> bool:
    """
    Main solving algorithm using recursive backtracking.
    
    The algorithm prioritizes placing queens in the most constrained positions
    (rows, columns, or colors that have the fewest valid placement options).
    
    Returns:
        bool: True if a solution was found, False otherwise
    """
    self.print_board()
    
    # Success condition: we've placed all queens
    if len(self.queens) == self.n:
      print(self.queens)
      return True
    
    # Count valid positions for each row, column, and color
    counter = Counter()
    
    for r in range(self.n):
      for c in range(self.n):
        # Check if position is valid for queen placement
        if not self.rows_solved[r] and not self.cols_solved[c] and not self.colors_solved[self.board[r][c]] and not self.is_near_queen(r, c):
          counter[f'row {r}'] += 1
          counter[f'col {c}'] += 1
          counter[f'color {self.board[r][c]}'] += 1
    
    if not counter: # No free positions
      print('No free positions')
      return False
    
    # Find the most constrained group (the one with fewest options)
    most_constrained_group = min(counter, key=counter.get)
    group_type, group_index = most_constrained_group.split(' ')
    group_index = int(group_index)
    print(f'Most constrained group: {most_constrained_group}')

    # Generate list of positions to try based on the most constrained group
    positions_to_try = []
    if group_type == 'row':
      positions_to_try = [(group_index, c) for c in range(self.n) if not self.cols_solved[c] and not self.colors_solved[self.board[group_index][c]] and not self.is_near_queen(group_index, c)]
    elif group_type == 'col':
      positions_to_try = [(r, group_index) for r in range(self.n) if not self.rows_solved[r] and not self.colors_solved[self.board[r][group_index]] and not self.is_near_queen(r, group_index)]
    elif group_type == 'color':
      positions_to_try = [(r, c) for r in range(self.n) for c in range(self.n) if not self.rows_solved[r] and not self.cols_solved[c] and not self.colors_solved[self.board[r][c]] and not self.is_near_queen(r, c)]
    
    # Try each position recursively
    for r, c in positions_to_try:
      self.place_queen(r, c)
      if self.solve():
        return True
      self.remove_queen(r, c)
    
    return False

if __name__ == '__main__':
  # Example board for testing
  board = [
    [1, 1, 3, 2, 0],
    [1, 1, 3, 2, 0],
    [0, 0, 3, 3, 0],
    [0, 0, 0, 3, 0],
    [0, 4, 0, 0, 0],
  ]
  # Solution:

  solver = QueensSolver(board)
  print(solver.solve())
