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

    def update_scroll(self, surface):
        """Center camera around the player"""
        # Center horizontally
        self.scroll[0] += ((self.player.rect().centerx - surface.get_width() / 2
                            - self.scroll[0]) / 30)
        # Center vertically
        self.scroll[1] += ((self.player.rect().centery - surface.get_height() / 2
                           - self.scroll[1]) / 30)

    def update_scroll_editor(self, movement):
        """Center the camera in the editor"""
        # Move horizontally
        self.scroll[0] += (movement[1] - movement[0]) * 2
        # Move vertically
        self.scroll[1] += (movement[3] - movement[2]) * 2
