import json
import math
import undetected_chromedriver as uc
from multiprocessing import freeze_support
import os
from humancursor import WebCursor
from selenium.webdriver.common.by import By

from linkedin_queens_bot.solver import QueensSolver

def main():
    # Check if cookies file exists, if not, create it by logging into LinkedIn
    if not os.path.exists('cookies.json'):
        driver = uc.Chrome(headless=False, use_subprocess=False)
        driver.get('https://www.linkedin.com/')
        input("Press Enter after you've logged in to LinkedIn (if needed)...")
        cookies = driver.get_cookies()
        driver.quit()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)
    
    # Initialize Chrome browser
    driver = uc.Chrome(headless=False, use_subprocess=False) # Change to be headless when done with development
    
    # Load saved cookies to avoid manual login
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    driver.get('https://www.linkedin.com/')
    for cookie in cookies:
        if "linkedin" in cookie['domain'].lower():
            driver.add_cookie(cookie)

    # Navigate to the Queens game page
    driver.get('https://www.linkedin.com/games/queens/')
    
    # Initialize human-like cursor movements
    # cursor = WebCursor(driver)
    # cursor.show_cursor()
    # Click the start button to begin the game
    start_button = None
    try:
        start_button = driver.find_element(By.ID, 'launch-footer-start-button')
    except:
        pass
    if start_button:
        # cursor.move_to(start_button)
        # cursor.click_on(start_button)
        start_button.click()

    # Check if tutorial is showing and skip it if present
    tutorial = None
    try:
        tutorial = driver.find_element(By.CLASS_NAME, 'queens-tutorial-modal')
    except:
        pass
    if tutorial:
        skip_button = tutorial.find_element(By.CSS_SELECTOR, '[data-test-modal-close-btn]')
        # cursor.move_to(skip_button)
        # cursor.click_on(skip_button)
        skip_button.click()

    # Get the game board and analyze its structure
    queens_board = driver.find_element(By.ID, 'queens-grid')
    queens_board_children = queens_board.find_elements(By.XPATH, '*')
    
    # Calculate board size (n x n)
    n = int(math.sqrt(len(queens_board_children)))
    print(f'Board size: {n}x{n}')
    
    # Initialize an empty board representation
    board = [[0 for _ in range(n)] for _ in range(n)]
    queens = []
    
    # Parse the board state and existing queens from the DOM
    for cell in queens_board_children:
        i = cell.get_attribute('data-cell-idx')
        if not i:
            continue
        i = int(i)
        r = i // n  # Row index
        c = i % n   # Column index
        
        # Extract the color information from cell classes
        classes = cell.get_attribute('class').split(' ')
        color = None
        for cls in classes:
            if cls.startswith('cell-color-'):
                color = int(cls.split('-')[-1])
                break
        board[r][c] = color
        
        # Identify cells that already have queens
        label = cell.get_attribute('aria-label')
        if label.startswith('Queen'):
            queens.append((r, c))
    
    # Initialize and run the solver algorithm
    solver = QueensSolver(board, queens)
    solver.solve()

    # Place queens on the board based on solver's solution
    for r, c in sorted(solver.queens):
        queen_on_cell(driver, r, c, n)

    # Take a screenshot of the solved board
    driver.save_screenshot('linkedin.png')
    input("Press Enter to quit...")
    driver.quit()

def queen_on_cell(driver, r, c, n):
    """
    Places a queen on the specified cell using human-like cursor movements.
    
    Args:
        cursor: The WebCursor instance for controlling mouse movement
        driver: The WebDriver instance
        r: Row index
        c: Column index
        n: Board size
    """
    cell = driver.find_element(By.XPATH, f'//*[@data-cell-idx="{r*n + c}"]')
    # cursor.move_to(cell)
    # cursor.click_on(cell)
    # cursor.click_on(cell)
    cell.click()
    cell.click()

if __name__ == '__main__':
    freeze_support()
    main()