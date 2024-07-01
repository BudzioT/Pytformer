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
        self.deco_tile_map = {}

        # Spawn grass and cobble for test
        for i in range(10):
            self.tile_map[str(3 + i) + ";10"] = \
                {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
            self.tile_map["10;" + str(5 + i)] = \
                {"type": "cobblestone", "variant": 1, "pos": (10, 5 + i)}

    def draw(self, surface, offset=(0, 0)):
        """Draw the tiles"""
        # Render tiles not affected by physics
        for tile in self.deco_tile_map:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]],
                         (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        # Render tiles affected by physics
        for location in self.tile_map:
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
