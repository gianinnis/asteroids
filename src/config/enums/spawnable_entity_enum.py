from enum import Enum
from src.entities.asteroid import Asteroid
from src.entities.diamond import Diamond

class SpawnableEntityEnum(Enum):
    ASTEROID = (Asteroid, 0.8, 20, 3)
    DIAMOND = (Diamond, 10, 12, 1)

    def __init__(self, entity_class, interval, min_radius, kinds):
        self.entity_class = entity_class
        self.interval = interval
        self.min_radius = min_radius
        self.kinds = kinds
        self.max_radius = min_radius * self.kinds