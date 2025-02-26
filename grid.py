import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    @property
    def rows(self):
        return self.num_rows

    @property
    def columns(self):
        return self.num_cols

    def draw(self, screen):
        darker_blue = (44, 44, 127)
        gray = (14, 14, 24) 
        grid_line_color = (20, 20, 60)
        
        screen.fill(gray)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                if cell_value != 0:
                    cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1,
                                            self.cell_size - 1, self.cell_size - 1)
                    pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

        for row in range(self.num_rows + 1):
            pygame.draw.line(screen, grid_line_color, (0, row * self.cell_size),
                             (self.num_cols * self.cell_size, row * self.cell_size))

        for col in range(self.num_cols + 1):
            pygame.draw.line(screen, grid_line_color, (col * self.cell_size, 0),
                             (col * self.cell_size, self.num_rows * self.cell_size))
            
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True 
        
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0
            
    def move_row_down(self, row, num_rows):
        if row + num_rows < self.num_rows:
            for column in range(self.num_cols):
                self.grid[row + num_rows][column] = self.grid[row][column]
                self.grid[row][column] = 0

            
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                if row + completed < self.num_rows:
                    self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def is_completely_empty(self):
        return all(all(cell == 0 for cell in row) for row in self.grid)


    def is_inside(self, row, column):
        return 0 <= row < self.num_rows and 0 <= column < self.num_cols
