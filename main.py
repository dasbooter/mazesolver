import time
import tkinter as tk
import random

class Cell:
    def __init__(self, x1, x2, y1, y2, canvas=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.canvas = canvas
        self.fill_color = None  # Add fill_color attribute

    def draw(self):
        if self.canvas is None:
            return  # Do nothing if canvas is not provided

        # Background color
        bg_color = "black" if self.fill_color is None else self.fill_color  # Use cell's fill_color
        wall_color = "white"  # Walls are white

        # Ensure coordinates are integers
        x1 = int(self.x1)
        x2 = int(self.x2)
        y1 = int(self.y1)
        y2 = int(self.y2)

        # Fill the cell with the specified background color
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

        # Draw left wall
        if self.has_left_wall:
            self.canvas.create_line(x1, y1, x1, y2, fill=wall_color, width=1)

        # Draw right wall
        if self.has_right_wall:
            self.canvas.create_line(x2, y1, x2, y2, fill=wall_color, width=1)

        # Draw top wall
        if self.has_top_wall:
            self.canvas.create_line(x1, y1, x2, y1, fill=wall_color, width=1)

        # Draw bottom wall
        if self.has_bottom_wall:
            self.canvas.create_line(x1, y2, x2, y2, fill=wall_color, width=1)

    def draw_move(self, to_cell, undo=False):
        if self.canvas is None:
            return  # Do nothing if canvas is not provided
        center_x1 = int((self.x1 + self.x2) / 2)
        center_y1 = int((self.y1 + self.y2) / 2)
        center_x2 = int((to_cell.x1 + to_cell.x2) / 2)
        center_y2 = int((to_cell.y1 + to_cell.y2) / 2)
        fill_color = "red" if undo else "yellow"  # Use yellow for the path
        self.canvas.create_line(
            center_x1, center_y1, center_x2, center_y2, fill=fill_color, width=2
        )

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            window=None,
            seed=None,
            generation_sleep_time=0.00001,
            solving_sleep_time=0.01
        ):
        if num_rows < 0 or num_cols < 0:
            raise ValueError("Number of rows and columns must be non-negative")
        if seed is not None:
            random.seed(seed)  # Seed the random number generator
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.canvas = window.canvas if window else None
        self.generation_sleep_time = generation_sleep_time
        self.solving_sleep_time = solving_sleep_time
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_iterative()  # Use the iterative version
        self._reset_cells_visited()  # Reset visited status of all cells

    def _create_cells(self):
        for i in range(self.num_cols):
            column = []
            self._cells.append(column)
            for j in range(self.num_rows):
                x1 = self.x1 + i * self.cell_size_x
                x2 = x1 + self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, x2, y1, y2, self.canvas)
                column.append(cell)
                # Draw the cell (without walls broken yet)
                cell.draw()
        self._animate(self.generation_sleep_time)

    def _animate(self, sleep_time=0.01):
        if self.window is None or not self.window.canvas_running:
            return False  # Window is closed, stop animation
        self.window.redraw()
        time.sleep(sleep_time)
        return True

    def _break_entrance_and_exit(self):
        # Break the top wall of the entrance cell (top-left cell)
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        entrance_cell.fill_color = "red"  # Set fill color to red
        entrance_cell.draw()
        self._animate(self.generation_sleep_time)

        # Break the bottom wall of the exit cell (bottom-right cell)
        exit_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        exit_cell.has_bottom_wall = False
        exit_cell.fill_color = "green"  # Set fill color to green
        exit_cell.draw()
        self._animate(self.generation_sleep_time)

    def _break_walls_iterative(self):
        stack = []
        i, j = 0, 0
        current_cell = self._cells[i][j]
        current_cell.visited = True
        stack.append((i, j, current_cell))

        while stack:
            if not self.window.canvas_running:
                break
            i, j, current_cell = stack[-1]  # Peek at the top of the stack

            # Find unvisited neighbors
            directions = []

            # North
            if j > 0 and not self._cells[i][j - 1].visited:
                directions.append(('N', i, j - 1))
            # South
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                directions.append(('S', i, j + 1))
            # West
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append(('W', i - 1, j))
            # East
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                directions.append(('E', i + 1, j))

            if directions:
                # Choose a random direction
                direction, next_i, next_j = random.choice(directions)

                # Knock down the wall between current cell and chosen cell
                next_cell = self._cells[next_i][next_j]
                if direction == 'N':
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                elif direction == 'S':
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                elif direction == 'W':
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
                elif direction == 'E':
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False

                # Draw the current cell and the next cell to update walls
                current_cell.draw()
                next_cell.draw()
                if not self._animate(self.generation_sleep_time):
                    break

                # Mark the next cell as visited and push it onto the stack
                next_cell.visited = True
                stack.append((next_i, next_j, next_cell))
            else:
                # Backtrack
                stack.pop()

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self._solve_iterative()

    def _solve_iterative(self):
        stack = []
        i, j = 0, 0
        current_cell = self._cells[i][j]
        current_cell.visited = True
        stack.append((i, j, current_cell))

        while stack:
            if not self.window.canvas_running:
                break
            i, j, current_cell = stack[-1]

            # If current cell is the exit cell, return True
            if i == self.num_cols - 1 and j == self.num_rows - 1:
                return True

            if not self._animate(self.solving_sleep_time):
                break

            # Define possible directions
            directions = []

            # North
            if not current_cell.has_top_wall and j > 0:
                directions.append(('N', i, j - 1))
            # South
            if not current_cell.has_bottom_wall and j < self.num_rows - 1:
                directions.append(('S', i, j + 1))
            # West
            if not current_cell.has_left_wall and i > 0:
                directions.append(('W', i - 1, j))
            # East
            if not current_cell.has_right_wall and i < self.num_cols - 1:
                directions.append(('E', i + 1, j))

            # Filter out visited cells
            directions = [
                (dir, next_i, next_j) for dir, next_i, next_j in directions
                if not self._cells[next_i][next_j].visited
            ]

            if directions:
                # Choose a direction
                direction, next_i, next_j = random.choice(directions)
                next_cell = self._cells[next_i][next_j]
                next_cell.visited = True

                # Draw move between current cell and next cell
                current_cell.draw_move(next_cell)
                if not self._animate(self.solving_sleep_time):
                    break

                # Push the next cell onto the stack
                stack.append((next_i, next_j, next_cell))
            else:
                # Backtrack
                stack.pop()
                if stack:
                    prev_i, prev_j, prev_cell = stack[-1]
                    # Draw undo move
                    prev_cell.draw_move(current_cell, undo=True)
                    if not self._animate(self.solving_sleep_time):
                        break

        # No path found
        return False

class Window:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Maze Solver")
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")  # Background black
        self.canvas.pack()
        self.canvas_running = True  # Set to True initially
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        while self.canvas_running:
            self.redraw()
            time.sleep(0.01)  # Adjust as necessary

    def close(self):
        self.canvas_running = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    win = Window(root, 1920, 1080)  # Adjust window size as needed
    cell_size_x = 20
    cell_size_y = 20
    num_cols = win.width // cell_size_x
    num_rows = win.height // cell_size_y

    maze = Maze(
        x1=0,
        y1=0,
        num_rows=num_rows,
        num_cols=num_cols,
        cell_size_x=cell_size_x,
        cell_size_y=cell_size_y,
        window=win,
        seed=None,
        generation_sleep_time=0.000,  # Slower maze generation
        solving_sleep_time=0.01      # Animation slowed down by half during solving
    )
    maze.solve()
    win.wait_for_close()
