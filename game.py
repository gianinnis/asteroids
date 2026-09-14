from game_state_enum import GameState

class Game:
    def __init__(self):
        self.state = GameState.TITLE

    def start(self):
        self.state = GameState.PLAYING

    def pause(self):
        self.state = GameState.PAUSED

    def over(self):
        self.state = GameState.GAME_OVER

    def restart(self, asteroids, shots, player, score_manager):
        for asteroid in asteroids:
            asteroid.kill()
        for shot in shots:
            shot.kill()
        player.reset()
        score_manager.reset()
        self.start()
