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
        self.pos[0] += pos_increase[0]
        # Save entity's rectangle
        rect = self.rect()

        # Add movement to the current position
        self.pos[1] += pos_increase[1]
        # Save entity's rectangle
        rect = self.rect()

    def draw(self, surface):
        """Draw the entity"""
        surface.blit(self.game.assets["player"], self.pos)

    def rect(self):
        """Return rectangle of entity"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
