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

    def update(self):
        """Update the spark"""
        # Update positions (cosines for x position, sinus for y position)
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        # Make the sparks slower each frame
        self.speed = max(0, self.speed - 0.1)
        # Return if frames ended (speed is 0 when frames end, so not 0(False) is True)
        return not self.speed

    def draw(self, surface, offset=(0, 0)):
        """Draw the spark"""
        # Calculate the points to draw a polygon with a diamond shape
        draw_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0],
             self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),

            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0],
             self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1]),

            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0],
             self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),

            (self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0],
             self.pos[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1])
        ]
        # Draw it
        pygame.draw.polygon(surface, (255, 255, 255), draw_points)
