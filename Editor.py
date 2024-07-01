import sys

import pygame

from src.Utilities import Utilities
from src.TileMap import TileMap


class Editor:
    """Level editor to help build maps for the game"""
    def __init__(self):
        """Initialize the editor"""
        # Initialize pygame
        pygame.init()

        # Set the caption
        pygame.display.set_caption("Map Editor")

        # Create game surface and render surface
        self.surface = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        # Tile map
        self.tile_map = TileMap(self)
        # Utilities
        self.utilities = Utilities()

        # Assets of the map editor
        self.assets = {
            # Tiles
            "grass": self.utilities.load_images("tiles/grass"),
            "cobblestone": self.utilities.load_images("tiles/cobblestone"),
            # Others
            "decorations": self.utilities.load_images("tiles/decorations")
        }

        # FPS timer
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the map editor"""
        while True:
            # Handle events
            self._get_events()

            # Make the game run in 60 FPS
            self.timer.tick(60)

    def _get_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            # Quit the editor on request
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If user clicks the mouse, handle the mouse button down events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown()

    def _update_surface(self):
        """Update the surface"""
        # Scale and blit the rendering surface to the main one
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Show all the changes
        pygame.display.update()

    def _handle_mousedown(self):
        """Handle mouse button down events"""
        pass


editor = Editor()
editor.run()
