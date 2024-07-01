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

        # Entity action
        self.action = ''
        self.set_action("idle")

        # Collision booleans
        self.collisions = {"Left": False, "Right": False, "Up": False, "Down": False}

        # Animation variables
        self.animation_offset = (-1, 0)
        self.flip_animation = False

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
                if pos_increase[0] < 0:
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

        # Set the correct entity animation direction based of movement
        if movement[0] > 0:
            self.flip_animation = False
        if movement[0] < 0:
            self.flip_animation = True

        # Gravity
        self.velocity[1] = min(4, self.velocity[1] + 0.1)

        # Stop accelerating while jumping or falling when there is a collision
        if self.collisions["Up"] or self.collisions["Down"]:
            self.velocity[1] = 0

        # Update the animation
        self.animation.update()

    def draw(self, surface, offset=(0, 0)):
        """Draw the entity"""
        surface.blit(pygame.transform.flip(
            self.animation.get_frame_image(), self.flip_animation, False),
                     (self.pos[0] - offset[0] + self.animation_offset[0],
                      self.pos[1] - offset[1] + self.animation_offset[1]))

    def rect(self):
        """Return rectangle of entity"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '_animations'][action].copy_animation()


class Player(PhysicsEntity):
    """The player entity"""
    def __init__(self, game, pos, size):
        """Initialize the player"""
        super().__init__(game, "player", pos, size)
        # Time in air
        self.air_time = 0

    def update(self, tile_map, movement=(0, 0)):
        """Update the player position"""
        super().update(tile_map, movement)

        # Increase the time in air
        self.air_time += 1

        # If the player is standing, reset the time in air
        if self.collisions["Down"]:
            self.air_time = 0

        # If the player is long in the air, set action to jump
        if self.air_time > 5:
            self.set_action("jump")

        # If user is in place, set action to idle
        if not movement[0]:
            self.set_action("idle")
        # If user isn't in place, set action to run
        else:
            self.set_action("run")
