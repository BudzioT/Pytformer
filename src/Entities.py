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

        # Collision booleans
        self.collisions = {"Left": False, "Right": False, "Up": False, "Down": False}

    def update(self, tile_map, movement=(0, 0)):
        """Update position of entity"""
        # Save movement, by increasing it by velocity
        pos_increase = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Reset the collisions
        self.collisions = {"Left": False, "Right": False, "Up": False, "Down": False}

        # Add movement to the current horizontal position
        self.pos[0] += pos_increase[0]
        # Save entity's rectangle
        rect = self.rect()

        # Go through each of nearby physics tiles
        for tile_rect in tile_map.physics_tiles_near(self.pos):
            # If there is a collision, handle it
            if rect.colliderect(tile_rect):
                # If player moves to the right, hug him to the wall
                if pos_increase[0] > 0:
                    rect.right = tile_rect.left
                    self.collisions["Right"] = True
                # If player moves to the left, hug him to the wall
                if pos_increase[1] < 0:
                    rect.left = tile_rect.right
                    self.collisions["Left"] = True
                # Update the position
                self.pos[0] = rect.x

        # Add movement to the current vertical position
        self.pos[1] += pos_increase[1]
        # Save entity's rectangle
        rect = self.rect()

        # Go through each of nearby physics tiles
        for tile_rect in tile_map.physics_tiles_near(self.pos):
            # If there is a collision handle it again
            if rect.colliderect(tile_rect):
                # If player falls on the tile, don't let him through it
                if pos_increase[1] > 0:
                    rect.bottom = tile_rect.top
                    self.collisions["Down"] = True
                # If player hit the tile, don't allow him to jump through it
                if pos_increase[1] < 0:
                    rect.top = tile_rect.bottom
                    self.collisions["Up"] = True
                # Update real position
                self.pos[1] = rect.y

        # Gravity
        self.velocity[1] = min(4, self.velocity[1] + 0.1)

        if self.collisions["Up"] or self.collisions["Down"]:
            self.velocity[1] = 0

    def draw(self, surface):
        """Draw the entity"""
        surface.blit(self.game.assets["player"], self.pos)

    def rect(self):
        """Return rectangle of entity"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
