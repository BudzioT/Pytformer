import os

import pygame


class Utilities:
    """Utilities for the game"""
    def __init__(self):
        # Absolute path to current directory
        self.BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        # Images directory
        self.IMG_PATH = os.path.join(self.BASE_PATH, "../dependencies/images/")

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
