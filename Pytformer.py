import sys
import os

import pygame

from src.Entities import PhysicsEntity
from src.Utilities import Utilities
from src.TileMap import TileMap
from src.Camera import Camera
from src.Clouds import Clouds
from src.Animation import Animation


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
            # Entities
            "player": self.utilities.load_image("entities/player.png"),
            # Tiles
            "grass": self.utilities.load_images("tiles/grass"),
            "cobblestone": self.utilities.load_images("tiles/cobblestone"),
            # Others
            "decorations": self.utilities.load_images("tiles/decorations"),
            "background": self.utilities.load_image("sky/background.png"),
            "clouds": self.utilities.load_images("sky/clouds/"),
            # Player animations
            "player_animations": {
                "jump": Animation(self.utilities.load_images("entities/player/jump"), 5),
                "idle": Animation(self.utilities.load_images("entities/player/idle"), 9),
                "run": Animation(self.utilities.load_images("entities/player/run"), 5),
                "slide": Animation(self.utilities.load_images("entities/player/slide")),
                "wall_slide": Animation(self.utilities.load_images("entities/player/wall_slide"))
            }
        }

        # Create player
        self.player = PhysicsEntity(self, "Player",
                                    (100, 100), (8, 15))
        # Clouds
        self.clouds = Clouds(self.assets["clouds"])

        # Create tile map
        self.tile_map = TileMap(self)

        # Camera
        self.camera = Camera(self)

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
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # Movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = True
        # Movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = True
        # Jump
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.velocity[1] = -3

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
        # Draw the clouds and sky
        self.display.blit(self.assets["background"], (0, 0))
        self.clouds.draw(self.display)

        # Draw the tile map
        self.tile_map.draw(self.display, self.camera.scroll)

        # Draw the player
        self.player.draw(self.display, self.camera.scroll)

        # Blit the rendering surface onto the main one, scale it
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Update the display surface
        pygame.display.update()

    def _update_pos(self):
        """Update positions of things"""
        # Update camera scroll
        self.camera.update_scroll(self.display)

        # Update the player
        self.player.update(self.tile_map,
                           (self.movement[1] - self.movement[0], 0))
        # Update clouds
        self.clouds.update()


# Only run the game with this file
if __name__ == "__main__":
    # Create the game instance and run it
    game = Pytformer()
    game.run()
