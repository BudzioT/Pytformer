import sys

import pygame

from src.Utilities import Utilities
from src.TileMap import TileMap
from src.Camera import Camera


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
        # Camera
        self.camera = Camera()

        # Assets of the map editor
        self.assets = {
            # Tiles
            "grass": self.utilities.load_images("tiles/grass"),
            "cobblestone": self.utilities.load_images("tiles/cobblestone"),
            # Others
            "decorations": self.utilities.load_images("tiles/decorations")
        }

        # Tile general variables
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Mouse position
        self.mouse_pos = pygame.mouse.get_pos()

        # Tile current variables
        self.tile_image = None
        self.tile_pos = (0, 0)
        self._update_tile()

        # Control variables
        self.click = False
        self.right_click = False
        self.shift = False
        self.grid = True

        # Movement
        self.movement = [False, False, False, False]

        # FPS timer
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the map editor"""
        while True:
            # Handle events
            self._get_events()

            # Update the surface
            self._update_surface()
            # Update positions
            self._update_pos()

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
                self._handle_mousedown(event)

    def _handle_mousedown(self, event):
        """Handle mouse button down events"""
        # Handle left click
        if event.button == 1:
            self.click = True
            # If the element is an off-grid one, place the decoration
            if not self.grid:
                self.tile_map.deco_tile_map.append({})


    def _update_surface(self):
        """Update the surface"""
        # Clean the surface
        self.display.fill((0, 0, 0))

        # Scale and blit the rendering surface to the main one
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Draw the tile map
        self.tile_map.draw(self.display, self.camera.scroll)

        # Draw current tile
        self._draw_current_tile()

        # Show all the changes
        pygame.display.update()

    def _update_pos(self):
        """Update position of things"""
        self.camera.update_scroll_editor(self.movement)

    def _update_tile(self):
        """Update and change the tile"""
        self.tile_group = 0
        self.tile_variant = 0
        # Get the current tile
        self.tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        # Make it see-through to help building
        self.tile_image.set_alpha(80)

        # Set the tile position based off grid
        tile_x = int((self.mouse_pos[0] + self.camera.scroll[0]) // self.tile_map.size)
        tile_y = int((self.mouse_pos[1] + self.camera.scroll[1]) // self.tile_map.size)
        self.tile_pos = (tile_x, tile_y)

    def _draw_current_tile(self):
        """Draw the tile based on few factors"""
        # Draw current tile on grid
        if self.grid:
            tile_x = self.tile_pos[0] * self.tile_map.size - self.camera.scroll[0]
            tile_y = self.tile_pos[1] * self.tile_map.size - self.camera.scroll[1]
            self.display.blit(self.tile_image, (tile_x, tile_y))
        # Draw current tile at mouse position
        else:
            self.display.blit(self.tile_image, self.mouse_pos)

        # Place the tiles
        self._place_tiles()
        self.display.blit(self.tile_image, (5, 5))

    def _place_tiles(self):
        """Place the chosen tiles"""
        pass


# Only run using this file
if __name__ == "__main__":
    # Create
    editor = Editor()
    editor.run()
