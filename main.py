import pygame
import sys
from game import Game
from logger import log_state, log_event
from src.config.constants import *
from src.config.enums.game_state_enum import *
from src.entities.player import Player
from src.entities.asteroid import Asteroid
from src.entities.shot import Shot
from src.entities.diamond import Diamond
from src.systems.spawn_system import SpawnSystem
from src.systems.score_system import ScoreSystem
import time

def main():
    start = time.time()
    print("Imports done:", time.time() - start)
    pygame.init()
    print("pygame initialized:", time.time() - start)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    title_font = pygame.font.Font(None, 64)
    subtitle_font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    diamonds = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    SpawnSystem.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Diamond.containers = (diamonds, updatable, drawable)

    spawn_system = SpawnSystem()
    score_manager = ScoreSystem()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game = Game()

    print("Setup done:", time.time() - start)
    while True:
        log_state()

        # EVENT HANDLING PHASE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if game.state == GameState.TITLE:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game.start()

                elif game.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.shoot(dt)
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        game.pause()

                elif game.state == GameState.PAUSED:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_p):
                        game.start()

                elif game.state == GameState.GAME_OVER:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r):
                        game.restart(asteroids, shots, player, score_manager)

        screen.fill("black")
        dt = clock.tick(60) / 1000

        # UPDATE PHASE
        if game.state == GameState.PLAYING:
            updatable.update(dt)

            if player.lives <= 0:
                print("Game over!")
                game.over()

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    asteroid.kill()
                    player.lives -= 1
                    print(f"Lives left: {player.lives}")
                    
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        score_manager.add_points(asteroid.points)
                        asteroid.split()

            for diamond in diamonds:
                if diamond.collides_with(player):
                    diamond.kill()
                    player.diamonds += 1
                    print(f"Diamonds: {player.diamonds}")

        # DRAWING PHASE
        if game.state == GameState.TITLE:
            draw_text(screen, "ASTEROIDS", title_font, (255, 255, 255), center_x, center_y - 40)
            draw_text(screen, "Press SPACE to Start", subtitle_font, (200, 200, 200), center_x, center_y + 30)

        elif game.state == GameState.PLAYING:
            for obj in drawable:
                obj.draw(screen)
            score_manager.draw(screen)

        elif game.state == GameState.PAUSED:
            # Draw frozen game objects first
            for obj in drawable:
                obj.draw(screen)
            score_manager.draw(screen)
            # Overlay pause banner
            draw_text(screen, "PAUSED", title_font, (255, 255, 0), center_x, center_y - 20)
            draw_text(screen, "Press ESC or P to Resume", subtitle_font, (255, 255, 255), center_x, center_y + 30)

        elif game.state == GameState.GAME_OVER:
            # Draw frozen game objects first
            for obj in drawable:
                obj.draw(screen)
            score_manager.draw(screen)
            # Overlay Game Over banner
            draw_text(screen, "GAME OVER", title_font, (255, 50, 50), center_x, center_y - 20)
            draw_text(screen, "Press R to Restart", subtitle_font, (255, 255, 255), center_x, center_y + 30)
        
        pygame.display.flip()

def draw_text(screen, text, font, color, center_x, center_y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(center_x, center_y))
    screen.blit(surface, rect)  

if __name__ == "__main__":
    main()
