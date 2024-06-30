import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, entity_pos, entity_size):
        """Initialize physics entity"""
        # Get reference to the game
        self.game = game

        # Set entity parameters
        self.type = entity_type
        self.pos = list(entity_pos)
        self.velocity = [0, 0]
        self.size = entity_size

    def update(self, movement=(0, 0)):
        """Update position of entity"""
        # Save movement, by increasing it by velocity
        pos_increase = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        # Add movement to the current position
        self.pos[0], self.pos[1] = pos_increase[0], pos_increase[1]

    def draw(self, surface):
        """Draw the entity"""
        pass
