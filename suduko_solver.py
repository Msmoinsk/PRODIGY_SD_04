import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def is_safe(self, row, col, num):
        # Check if 'num' is not in the current row and column
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False

        # Check the 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True  # Puzzle solved

        row, col = empty

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                # Backtrack
                self.grid[row][col] = 0

        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI components."""
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 24), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=0, columnspan=9, pady=10)

        # Configure grid weights for responsiveness
        for i in range(9):
            self.root.rowconfigure(i, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(8, weight=1)

    def solve_sudoku(self):
        """Solve the Sudoku puzzle."""
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit() and value != '':
                    self.grid[i][j] = int(value)
                else:
                    self.grid[i][j] = 0

        solver = SudokuSolver(self.grid)
        if solver.solve():
            self.update_grid()
        else:
            messagebox.showinfo("No Solution", "This Sudoku puzzle cannot be solved.")

    def update_grid(self):
        """Update the GUI with the solved Sudoku grid."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()