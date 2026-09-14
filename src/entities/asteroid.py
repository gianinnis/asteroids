import pygame
import random
from logger import log_event
from src.entities.circleshape import CircleShape
from src.config.constants import *



class Asteroid(CircleShape):
    def __init_(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        first_vector = self.velocity.rotate(new_angle)
        second_vector = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_vector * 1.2
        second_asteroid.velocity = second_vector * 1.2

    @property
    def points(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 200
        if self.radius >= ASTEROID_MAX_RADIUS:
            return 50
        return 100
