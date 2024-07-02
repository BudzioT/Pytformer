import sys
import os

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
            # Spawners
            "spawners": self.utilities.load_images("tiles/spawners"),
            # Others
            "decorations": self.utilities.load_images("tiles/decorations"),
            "big_decorations": self.utilities.load_images("tiles/big_decorations")
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

        # Load the level map if it exists
        try:
            self.tile_map.load(os.path.join(self.utilities.BASE_PATH, "../dependencies/data/level.json"))
        # Continue if file is not found
        except FileNotFoundError:
            pass

        # FPS timer
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the map editor"""
        while True:
            # Update the surface
            self._update_surface()
            # Handle events
            self._get_events()
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
                # Handle scroll events too
                self._handle_scroll(event)
            # If user doesn't click the mouse anymore, handle mouse button up events
            if event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouseup(event)

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            # Handle key up events
            if event.type == pygame.KEYUP:
                self._handle_keyup(event)

    def _handle_mousedown(self, event):
        """Handle mouse button down events"""
        # Handle left click
        if event.button == 1:
            self.click = True
        # Handle right click
        if event.button == 3:
            # Set right click to true, informing that user wants to delete something
            self.right_click = True

    def _handle_scroll(self, event):
        """Handle scroll events"""
        # Handle shift hold with scroll (changing variants instead of groups)
        if self.shift:
            # Scroll up - change the variant up by one (modulo to ensure that index is in range)
            if event.button == 4:
                self.tile_variant = ((self.tile_variant + 1) %
                                     len(self.assets[self.tile_list[self.tile_group]]))
            # Scroll down
            if event.button == 5:
                self.tile_variant = ((self.tile_variant - 1) %
                                     len(self.assets[self.tile_list[self.tile_group]]))
        # Handle scroll without shift (change groups)
        else:
            # Scroll up - change group up by one
            if event.button == 4:
                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                # Reset variant to remain valid index
                self.tile_variant = 0
            # Scroll down
            if event.button == 5:
                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                # Reset variant to remain valid index
                self.tile_variant = 0

        # If the element is an off-grid one, place the decoration
        if self.click and not self.grid:
            # Get the group, variant and position
            group = self.tile_list[self.tile_group]
            variant = self.tile_variant
            pos = (self.mouse_pos[0] + self.camera.scroll[0], self.mouse_pos[1] +
                    self.camera.scroll[1])
            # Save them into JSON format
            self.tile_map.deco_tile_map.append({"type": group, "variant": variant, "pos": pos})

    def _handle_mouseup(self, event):
        """Handle mouse button up events"""
        # User stopped clicking left button
        if event.button == 1:
            self.click = False
        # User stopped clicking right button
        if event.button == 3:
            self.right_click = False

    def _handle_keydown(self, event):
        """Handle key down events"""
        # Quit on escape pressed
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # Movement to left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = True
        # Movement to right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = True
        # Movement up
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.movement[2] = True
        # Movement down
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.movement[3] = True

        # Change to on or off-grid placement with tab
        if event.key == pygame.K_TAB:
            self.grid = not self.grid
        # Change variants by holding shift
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            self.shift = True
        # Turn on auto-tiling with f key (it is close to movement, so it's more comfortable)
        if event.key == pygame.K_f:
            self.tile_map.auto_tile()
        # Save the changes by clicking return (or enter)
        if event.key == pygame.K_RETURN:
            self.tile_map.save(os.path.join(self.utilities.BASE_PATH, "../dependencies/data/level.json"))

    def _handle_keyup(self, event):
        """Handle key up events"""
        # Stop moving left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = False
        # Stop moving right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = False
        # Stop moving up
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.movement[2] = False
        # Stop moving down
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.movement[3] = False

    def _update_surface(self):
        """Update the surface"""
        # Clean the surface
        self.display.fill((0, 0, 0))

        # Draw the tile map
        self.tile_map.draw(self.display, self.camera.scroll)

        # Draw current tile
        self._draw_current_tile()

        # Scale and blit the rendering surface to the main one
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Show all the changes
        pygame.display.update()

    def _update_pos(self):
        """Update position of things"""
        # Update camera scroll
        self.camera.update_scroll_editor(self.movement)
        # Update mouse position
        self._get_mouse_pos()
        # Update tiles
        self._update_tile()
        # Place tiles
        self._place_tiles()

    def _update_tile(self):
        """Update and change the tile"""
        # Get the current tile
        self.tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        # Make it see-through to help building
        self.tile_image.set_alpha(140)

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
        # Place the tiles on a grid
        if self.click and self.grid:
            # Get the group, variant and position
            group = self.tile_list[self.tile_group]
            variant = self.tile_variant
            pos = self.tile_pos
            # Format the index
            formatted_index = str(self.tile_pos[0]) + ';' + str(self.tile_pos[1])
            self.tile_map.tile_map[formatted_index] = {"type": group, "variant": variant,
                                                       "pos": pos}
        # Remove the tiles on right click
        if self.right_click:
            self._remove_tiles()

    def _remove_tiles(self):
        """Remove the existing tiles on right click"""
        # Write location as JSON position
        tile_location = str(self.tile_pos[0]) + ';' + str(self.tile_pos[1])
        # If it's on grid, delete it
        if tile_location in self.tile_map.tile_map:
            del self.tile_map.tile_map[tile_location]
        # Delete the off-grid tiles
        for tile in self.tile_map.deco_tile_map.copy():
            # Save the image of current tile
            tile_img = self.assets[tile["type"]][tile["variant"]]
            # Calculate its position in the world
            rect_x = tile["pos"][0] - self.camera.scroll[0]
            rect_y = tile["pos"][1] - self.camera.scroll[1]
            # Create a rectangle for collision detection
            tile_rect = pygame.Rect(rect_x, rect_y, tile_img.get_width(), tile_img.get_height())
            # If mouse collides with tile, delete it
            if tile_rect.collidepoint(self.mouse_pos):
                self.tile_map.deco_tile_map.remove(tile)

    def _get_mouse_pos(self):
        """Get mouse position"""
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = (self.mouse_pos[0] / self.utilities.RENDER_SCALE,
                          self.mouse_pos[1] / self.utilities.RENDER_SCALE)


# Only run using this file
if __name__ == "__main__":
    # Create
    editor = Editor()
    editor.run()
