import pygame
import random
from logger import log_event
from src.entities.circleshape import CircleShape
from src.config.constants import *



class Diamond(CircleShape):
    def __init_(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt
