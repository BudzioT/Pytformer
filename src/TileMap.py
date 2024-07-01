class TileMap:
    """Map of tiles"""
    def __init__(self, game, size=16):
        """Initialize the map of tiles"""
        # Get game reference
        self.game = game

        # Title size
        self.size = size
        # Tile map affected by physics
        self.tile_map = {}
        # Tiles not affected by physics
        self.deco_tile_map = {}

        for i in range(10):
            self.tile_map[str(3 + i) + ";10"] = \
                {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
            self.tile_map[";10" + str(5 + i)] = \
                {"type": "cobblestone", "variant": 1, "pos": (10, 5 + i)}

    def draw(self, surface):
        """Draw the tiles"""
        # Render tiles not affected by physics
        for tile in self.deco_tile_map:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], tile["pos"])

        # Render tiles affected by physics
        for location in self.tile_map:
            tile = self.tile_map[location]
            surface.blit(self.game.assets[tile["type"]][tile["variant"]],
                         (tile["pos"][0] * self.size, tile["pos"][1] * self.size))

