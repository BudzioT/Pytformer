import sys
import os

import pygame

from src.Entities import  PhysicsEntity
from src.Utilities import Utilities
from src.TileMap import TileMap


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
        # Render help display
        self.display = pygame.Surface((320, 240))
        # Game utilities
        self.utilities = Utilities()

        # Movement of player
        self.movement = [False, False]

        # Assets of the game
        self.assets = {
            "player": self.utilities.load_image("entities/player.png"),
            "grass": self.utilities.load_images("tiles/grass"),
            "decorations": self.utilities.load_images("tiles/decorations"),
            "cobblestone": self.utilities.load_images("tiles/cobblestone")
        }

        print(self.assets)

        # Create player
        self.player = PhysicsEntity(self, "Player",
                                    (100, 100), (8, 15))
        # Create tile map
        self.tile_map = TileMap(self)

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
            # Update positions
            self._update_pos()
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
            if event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            # Handle keyup events
            if event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

    def _handle_keydown_events(self, event):
        """Handle keydown events"""
        # Movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = True
        # Movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = True
        # Jump
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.velocity[1] = -4

    def _handle_keyup_events(self, event):
        """Handle keyup events"""
        # End movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = False
        # End movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = False

    def _update_surface(self):
        """Update the surface"""
        # Clean the surface
        self.display.fill((2, 2, 2))

        # Draw the tile map
        self.tile_map.draw(self.display)

        # Draw the player
        self.player.draw(self.display)

        # Blit the rendering surface onto the main one, scale it
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Update the display surface
        pygame.display.update()

    def _update_pos(self):
        """Update positions of things"""
        # Update the player
        self.player.update((self.movement[1] - self.movement[0], 0))


# Only run the game with this file
if __name__ == "__main__":
    # Create the game instance and run it
    game = Pytformer()
    game.run()
