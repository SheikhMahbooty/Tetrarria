import pygame, sys
from game import Game
from colors import Colors

pygame.init()
pygame.key.set_repeat(100, 50)

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("Game Over!", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetrarria")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_s and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_w and game.game_over == False:
                game.hard_drop()
            if event.key == pygame.K_c and game.game_over == False:
                game.hold_block()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.rotate_counter_clockwise()
                
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
        
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        
        game.draw(screen) 
        game.draw_ghost_block(screen)
        game.draw_held_block(screen)

        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))
        
        if game.game_over == True:
            screen.blit(game_over_surface, (320, 300, 50, 50))
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(
            centerx = score_rect.centerx, centery = score_rect.centery
            ))

        pygame.display.update()
        clock.tick(60)