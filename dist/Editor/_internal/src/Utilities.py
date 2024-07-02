import os

import pygame


class Utilities:
    """Utilities for the game"""
    def __init__(self):
        # Absolute path to current directory
        self.BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        # Images directory
        self.IMG_PATH = os.path.join(self.BASE_PATH, "../dependencies/images/")
        # Near offsets of grid tiles
        self.NEAR_OFFSETS = [(0, 0), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1),
                             (1, -1), (1, 0), (1, 1)]
        # Tiles affected by physics
        self.PHYSICS_TILES = {"grass", "cobblestone"}
        # Tiles that can be affected by auto-tiling
        self.AUTO_TILE_TILES = {"grass", "cobblestone"}
        # Render scale for rendering surface
        self.RENDER_SCALE = 2

        # Auto tile rules
        self.AUTO_TILE_RULES = {
            # If tiles are everywhere around, place plain tile
            tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)])): 0,
            # If tiles are around but not on the left side, place left-end plain tile
            tuple(sorted([(1, 0), (0, -1), (0, 1)])): 1,
            # If tiles are around but not on the left and bottom, place left-end bottom plain tile
            tuple(sorted([(1, 0), (0, -1)])): 2,
            # If tiles are around but not on the right side, place right-end plain tile
            tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
            # If tiles are around but not on the right and bottom, place right-end bottom plain tile
            tuple(sorted([(-1, 0), (0, -1)])): 4,
            # If tiles are everywhere but not on the top, place normal top tile
            tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 5,
            # If this is the top-right tile, place it
            tuple(sorted([(-1, 0), (0, 1)])): 6,
            # If this is the top-left tile, place it
            tuple(sorted([(1, 0), (0, 1)])): 7
        }

    def load_image(self, directory):
        """Load and return the image"""
        image = pygame.image.load(self.IMG_PATH + directory).convert_alpha()
        return image

    def load_images(self, directory):
        """Load multiple images"""
        images = []
        # Go through every image in directory, load it and append to the images list
        for image in os.listdir(self.IMG_PATH + directory):
            images.append(self.load_image(directory + '/' + image))
        return images
