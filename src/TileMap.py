import json

import pygame

from src.Utilities import Utilities


class TileMap:
    """Map of tiles"""
    def __init__(self, game, size=16):
        """Initialize the map of tiles"""
        # Get game reference
        self.game = game
        # Utilities
        self.utilities = Utilities()

        # Title size
        self.size = size
        # Tile map affected by physics
        self.tile_map = {}
        # Tiles not affected by physics
        self.deco_tile_map = []

    def draw(self, surface, offset=(0, 0)):
        """Draw the tiles"""
        # Render tiles not affected by physics (off-grid ones)
        for tile in self.deco_tile_map:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]],
                         (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        # Calculate the position of the first visible tile and last one horizontally
        range_x = (int(offset[0] // self.size),
                   int((offset[0] + surface.get_width()) // self.size + 1))
        # Vertically
        range_y = (int(offset[1] // self.size),
                   int((offset[1] + surface.get_height()) // self.size + 1))

        # Render tiles affected by physics, only the visible ones (grid)
        for pos_x in range(range_x[0], range_x[1]):
            for pos_y in range(range_y[0], range_y[1]):
                location = str(pos_x) + ';' + str(pos_y)
                # If the tile exists, draw it
                if location in self.tile_map:
                    tile = self.tile_map[location]
                    surface.blit(self.game.assets[tile["type"]][tile["variant"]],
                                 (tile["pos"][0] * self.size - offset[0],
                                  tile["pos"][1] * self.size - offset[1]))

    def _get_tiles_near(self, pos):
        """Return tiles near the given position"""
        tiles = []
        # Get tile location in grid
        tile_location = (int(pos[0] // self.size), int(pos[1] // self.size))
        # Look for every near offset possible
        for offset in self.utilities.NEAR_OFFSETS:
            # Change location to the JSON grid format, add offset to it
            location = (str(tile_location[0] + offset[0]) + ';' +
                        str(tile_location[1] + offset[1]))
            # If the location is pointing to a tile, append it to the list
            if location in self.tile_map:
                tiles.append(self.tile_map[location])
        return tiles

    def physics_tiles_near(self, pos):
        """Return near physics tiles as rectangles"""
        tiles = []
        # Search for every tile near
        for tile in self._get_tiles_near(pos):
            # If it is a physic tiles, convert it to a rectangle and append to the list
            if tile["type"] in self.utilities.PHYSICS_TILES:
                tiles.append(pygame.Rect(tile["pos"][0] * self.size,
                                         tile["pos"][1] * self.size,
                                         self.size, self.size))
        return tiles

    def save(self, path):
        """Save all changes to a given file"""
        # Open file in write mode
        with open(path, "w") as file:
            # Dump the tile map variables in JSON format
            json.dump(
                {"tile_map": self.tile_map, "tile_size": self.size, "off_grid": self.deco_tile_map}, file)

    def load(self, path):
        """Load changes from a given file"""
        # Open file in read mode
        with open(path, "r") as file:
            # Save the data from JSON format
            data = json.load(file)
        # Save all information
        self.tile_map = data["tile_map"]
        self.size = data["tile_size"]
        self.deco_tile_map = data["off_grid"]

    def auto_tile(self):
        """Change variants depending on the placement automatically"""
        # Go through each tile location in map
        for location in self.tile_map:
            # Get the tile based of location
            tile = self.tile_map[location]
            near_tiles = set()
            # Go through each near tile
            for near in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Calculate the near tile location in JSON format
                near_location = str(tile["pos"][0] + near[0]) + ';' + str(tile["pos"][1] + near[1])
                # If there is a tile and not just empty space, add it to the near tiles set
                if near_location in self.tile_map:
                    near_tiles.add(near)
            # Sort them for auto tile rules checking
            near_tiles = tuple(sorted(near_tiles))
            # If this group of tiles is affected by auto-tiling and a rule applies, change its variant
            if (tile["type"] in self.utilities.AUTO_TILE_TILES) and (near_tiles
                                                                     in self.utilities.AUTO_TILE_RULES):
                tile["variant"] = self.utilities.AUTO_TILE_RULES[near_tiles]

    def extract(self, id_pairs, keep=False):
        """Get all tiles from given pairs, remove them if needed"""
        matches = []
        # Go through each off-grid tile
        for tile in self.deco_tile_map.copy():
            # If tile is in pair, append it to the list
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                # If it isn't needed, remove it
                if not keep:
                    self.deco_tile_map.remove(tile)

        # Go through each grid tile
        for location in self.tile_map:
            tile = self.tile_map[location]
            # If tile is in pair, append it to the list
            if (tile["type"], tile["variant"]) in id_pairs:
                # Get the copy
                matches.append(tile.copy())
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                # Convert size to pixels
                matches[-1]["pos"][0] *= self.size
                matches[-1]["pos"][1] *= self.size
                # If it isn't needed anymore remove it
                if not keep:
                    del self.tile_map[location]

        return matches
