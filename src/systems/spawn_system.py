import pygame
import random
from collections.abc import Callable
from src.config.enums.spawnable_entity_enum import SpawnableEntityEnum
from src.config.constants import *

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class SpawnSystem(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timers = {entity: 0.0 for entity in SpawnableEntityEnum}

    def _spawn(
        self, entity: SpawnableEntityEnum
    ) -> None:
        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, entity.kinds)
        radius = entity.min_radius * kind

        spawned = entity.entity_class(position.x, position.y, radius)
        spawned.velocity = velocity

    def update(self, dt: float) -> None:
        for entity in SpawnableEntityEnum:
            self.timers[entity] += dt

            if self.timers[entity] >= entity.interval:
                self.timers[entity] = 0.0
                self._spawn(entity)