import sys
import os

import pygame

from Entities import PhysicsEntity


class Pytformer:
    """Pytformer - a Python platformer"""
    def __init__(self):
        """Initialize the game"""
        # Initialize pygame
        pygame.init()

        # Set caption
        pygame.display.set_caption("Pytformer")

        # Game surface
        self.surface = pygame.display.set_mode((640, 480))

        # Movement of player
        self.movement = [False, False]

        # Create player
        self.player = PhysicsEntity(self, "Player",
                                    (100, 0), (10, 18))

        # FPS timer
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the game"""
        # Game loop
        while True:
            # Handle the events
            self._get_events()
            # Update the surface
            self._update_surface()
            # Run the game in 60 FPS
            self.timer.tick(60)

    def _get_events(self):
        """Get the input events"""
        # Go through each event
        for event in pygame.event.get():
            # If event is quit request, quit the game
            if event.type == pygame.QUIT:
                # Free the pygame resources
                pygame.quit()
                sys.exit()
            # Handle keydown events
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            # Handle keyup events
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

    def _handle_keydown_events(self, event):
        """Handle keydown events"""
        # Movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = True
        # Movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = True
        # Movement to the top
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.movement[0] = False
        # Movement to the bottom
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.movement[1] = False

    def _handle_keyup_events(self, event):
        """Handle keyup events"""
        pass

    def _update_surface(self):
        """Update the surface"""

        # Update the player
        self.player.update((self.movement[1] - self.movement[0], 0))

        # Update the display surface
        pygame.display.update()


# Only run the game with this file
if __name__ == "__main__":
    # Create the game instance and run it
    game = Pytformer()
    game.run()
