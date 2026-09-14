import pygame
from src.config.constants import *

class ScoreSystem:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.score = 0
        self.high_score = self._load_high_score()
        self.font = pygame.font.Font(None, 36)
    
    def _load_high_score(self):
        try:
            with open(self.filename, "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def _save_high_score(self):
        with open(self.filename, "w") as file:
            file.write(str(self.high_score))
    
    def add_points(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()

    def reset(self):
        self.score = 0

    def draw(self, screen):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))

        screen.blit(score_surface, (10, 10))
        screen.blit(high_score_surface, (10, 45))

    