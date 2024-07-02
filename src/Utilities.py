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
        # Render scale for rendering surface
        self.RENDER_SCALE = 2
        # Auto tile rules
        self.AUTO_TILE_RULES = {
            tuple(sorted([(1, 0), (0, 1)])): 7,
            tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 5,
            tuple(sorted([(-1, 0), (0, 1)])): 6
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
