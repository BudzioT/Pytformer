import math

import pygame

class Spark:
    """Class representing single spark"""
    def __init__(self, pos, angle, speed):
        """Initialize spark"""
        # Set position variables
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
