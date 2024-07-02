import random


class Camera:
    def __init__(self, game=None):
        """Initialize the camera"""
        # Game reference
        self.game = game
        # Player reference
        if game:
            self.player = game.player

        # Camera movement scroll
        self.scroll = [0, 0]

        # Screen shake
        self.screen_shake = 0
        # Its offset
        self.screen_shake_offset = (random.random() * self.screen_shake - self.screen_shake / 2,
                                    random.random() * self.screen_shake - self.screen_shake / 2)

    def update_scroll(self, surface):
        """Center camera around the player"""
        # Center horizontally
        self.scroll[0] += ((self.player.rect().centerx - surface.get_width() / 2
                            - self.scroll[0]) / 30)
        # Center vertically
        self.scroll[1] += ((self.player.rect().centery - surface.get_height() / 2
                           - self.scroll[1]) / 30)
        # Decrease screen shake until 0
        self.screen_shake = max(0, self.screen_shake - 1)

        # Calculate screen shake offset
        self.screen_shake_offset = (random.random() * self.screen_shake - self.screen_shake / 2,
                                    random.random() * self.screen_shake - self.screen_shake / 2)

    def update_scroll_editor(self, movement):
        """Center the camera in the editor"""
        # Move horizontally
        self.scroll[0] += (movement[1] - movement[0]) * 2
        # Move vertically
        self.scroll[1] += (movement[3] - movement[2]) * 2
