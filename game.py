from grid import Grid
from blocks import *
import pygame, random, time

held_block = None

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.held_block: Optional[Block] = None
        self.can_hold: bool = True
        
        self.last_hard_drop_time = 0
        self.hard_drop_cooldown = 100
        self.last_rotation_time = 0 
        self.rotation_delay = 150 
        self.game_over = False
        self.score = 0
        
        self.rotate_sound = pygame.mixer.Sound("../Tetrarria/sounds/rotate.wav")
        self.clear_line = pygame.mixer.Sound("../Tetrarria/sounds/clearline.wav")
        self.placement_sound = pygame.mixer.Sound("../Tetrarria/sounds/hit.wav")
        self.combo_1 = pygame.mixer.Sound("../Tetrarria/sounds/combo_1_power.wav")
        self.combo_2 = pygame.mixer.Sound("../Tetrarria/sounds/combo_2_power.wav")
        self.combo_3 = pygame.mixer.Sound("../Tetrarria/sounds/combo_1_power.wav")
        self.combo_4 = pygame.mixer.Sound("../Tetrarria/sounds/combo_4_power.wav")
        self.allclear = pygame.mixer.Sound("../Tetrarria/sounds/allclear.wav")
        self.harddrop = pygame.mixer.Sound("../Tetrarria/sounds/harddrop.wav")
        pygame.mixer.music.load("../Tetrarria/sounds/bg.ogg")
        pygame.mixer.music.set_volume(0)  
        pygame.mixer.music.play(-1)

    def hold_block(self):
        if not self.can_hold:
            return
        if self.held_block is None:
            self.held_block = self.current_block
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        else:
            self.current_block, self.held_block = self.held_block, self.current_block
        if hasattr(self.held_block, 'reset_rotation'):
            self.held_block.reset_rotation() 
        if hasattr(self.current_block, 'reset_rotation'):
            self.current_block.reset_rotation()
            self.current_block.row_offset = 0
        self.current_block.column_offset = self.grid.columns // 2 - 2
        self.held_block.row_offset = 0
        self.held_block.column_offset = self.grid.columns // 2 - 2
        self.can_hold = False

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(),
                           OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def lock_block(self, placement_points=5):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.current_block.row_offset = 0
        self.current_block.column_offset = self.grid.columns // 2 - 2
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, placement_points)
        self.can_hold = True
        if not self.block_fits():
            self.game_over = True
            
    def draw_held_block(self, screen):
        if self.held_block is None:
            return
        held_block_tiles = self.held_block.get_cell_positions()
        cell_size = self.grid.cell_size
        held_block_offset_x = 270
        held_block_offset_y = 400

        for tile in held_block_tiles:
            pygame.draw.rect(
                screen,
                self.held_block.colors[self.held_block.id],
                pygame.Rect(
                    tile.column * cell_size + held_block_offset_x,
                    tile.row * cell_size + held_block_offset_y,
                    cell_size - 1,
                    cell_size - 1
                )
            )

    def update_score(self, lines_cleared, placement_points=0):
        if lines_cleared == 1:
            self.score += 100
            self.combo_1.play()
        elif lines_cleared == 2:
            self.score += 300
            self.combo_2.play()
        elif lines_cleared == 3:
            self.score += 500
            self.combo_3.play()
        elif lines_cleared == 4:
            self.score += 1000
            self.combo_4.play()
        elif self.grid.is_completely_empty():
            self.score += 5000 
            self.allclear.play()
        else:
            self.placement_sound.play()
        self.score += placement_points

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.held_block = None
        self.score = 0
        self.can_hold = True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def rotate(self):
        current_time = time.time() * 1000
        if current_time - self.last_rotation_time >= self.rotation_delay:
            self.current_block.rotate()
            if not self.block_inside() or not self.block_fits():
                self.current_block.undo_rotation()
            else:
                self.rotate_sound.play()
            self.last_rotation_time = current_time  
            
    def rotate_counter_clockwise(self):
        self.current_block.rotate(counter_clockwise=True)
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.set_volume(0.3)
            self.rotate_sound.play()


    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True
            
    def draw(self, screen):
        self.grid.draw(screen)
        for tile in self.current_block.get_cell_positions():
            pygame.draw.rect(
                screen,
                self.current_block.colors[self.current_block.id],
                pygame.Rect(
                    tile.column * self.grid.cell_size,
                    tile.row * self.grid.cell_size,
                    self.grid.cell_size - 1,
                    self.grid.cell_size - 1
                )
            )

        next_block_tiles = self.next_block.get_cell_positions()
        cell_size = self.grid.cell_size
        next_block_offset_x = 270 
        next_block_offset_y = 230

        for tile in next_block_tiles:
            pygame.draw.rect(
                screen,
                self.next_block.colors[self.next_block.id],
                pygame.Rect(
                    tile.column * cell_size + next_block_offset_x,
                    tile.row * cell_size + next_block_offset_y,
                    cell_size - 1,
                    cell_size - 1
                )
            )
    def hard_drop(self):
        if hasattr(self, 'last_hard_drop') and time.time() - self.last_hard_drop < 0.2:
            return
        self.last_hard_drop = time.time()
        max_drop = 0
        while True:
            positions = self.current_block.get_cell_positions()
            if all(self.grid.is_inside(pos.row + max_drop + 1, pos.column) and 
                   self.grid.is_empty(pos.row + max_drop + 1, pos.column)
                   for pos in positions):
                max_drop += 1
            else:
                break
        if max_drop > 0:
            self.current_block.move(max_drop, 0)

        pygame.mixer.Sound("../Tetrarria/sounds/harddrop.wav").play()
        self.lock_block()
        
    def draw_ghost_block(self, screen):
        ghost_block = self.current_block
        max_drop = 0
        while True:
            positions = ghost_block.get_cell_positions()
            if all(self.grid.is_inside(pos.row + max_drop + 1, pos.column) and 
                   self.grid.is_empty(pos.row + max_drop + 1, pos.column)
                   for pos in positions):
                max_drop += 1
            else:
                break

        for pos in positions:
            ghost_tile = pygame.Rect(pos.column * self.grid.cell_size,
                                     (pos.row + max_drop) * self.grid.cell_size,
                                     self.grid.cell_size - 1, self.grid.cell_size - 1)
            pygame.draw.rect(screen, (200, 200, 200), ghost_tile, 1)             
