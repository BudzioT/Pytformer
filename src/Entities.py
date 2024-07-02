import random
import math

import pygame

from src.Particle import Particle


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

        # Last entity's movement
        self.last_movement = [0, 0]

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

        # Save the movement
        self.last_movement = movement

        # Gravity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

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

        # Jumps limit
        self.jumps = 1
        # Dash
        self.dashing = 0

        # Wall slide flag
        self.wall_slide = False

    def update(self, tile_map, movement=(0, 0)):
        """Update the player position"""
        super().update(tile_map, movement)

        # Increase the time in air
        self.air_time += 1

        # If the player is standing, reset the time in air
        if self.collisions["Down"]:
            self.air_time = 0
            # Reset the jumps
            self.jumps = 1

        # Set wall slide flag to False
        self.wall_slide = False

        # If player collides with wall and is in the air, turn on the wall slide
        if (self.collisions["Left"] or self.collisions["Right"]) and self.air_time > 4:
            self.wall_slide = True
            # Limit the fall velocity to 0.5
            self.velocity[1] = min(self.velocity[1], 0.5)

            # Set the direction of sliding to the correct one
            if self.collisions["Right"]:
                # If player slides off the right wall, don't flip the image (default is facing right)
                self.flip_animation = False
            # Else flip it to the left
            else:
                self.flip_animation = True
            self.set_action("wall_slide")

        # If user is not sliding, change the action to the correct one
        if not self.wall_slide:
            # If the player is long in the air, set action to jump
            if self.air_time > 4:
                self.set_action("jump")

            # If user is in place, set action to idle
            if not movement[0]:
                self.set_action("idle")
            # If user isn't in place, set action to run
            else:
                self.set_action("run")

        # If the players is dashing in the first 10 frames (dash time), create 15 particles
        if abs(self.dashing) in {60, 50}:
            # Create 15 particles
            for particle_num in range(15):
                # Calculate the angle, speed and velocity of particles
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                # Create a particle with calculated variables
                self.game.particles.append(Particle(self.game, "normal",
                                                    self.rect().center, particle_velocity,
                                                    random.randint(0, 7)))

        # If player is dashing to the right, decrease the dashing time
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        # If player is dashing to the left, decrease the time
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        # If it's the first 10 frame of dash, set the dash velocity to high one
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            # Stop the dash at 9th frame
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

            # Make the particle velocity a little random
            particle_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            # Spawn the particles at the center of player position, with particle velocity, at random frame
            self.game.particles.append(Particle(self.game, "normal", self.rect().center,
                                                particle_velocity, random.randint(0, 7)))

        # If player velocity is in the right direction, slowly decrease it
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        # Do it for the left too
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def draw(self, surface, offset=(0, 0)):
        """Draw the player"""
        # If dashing ended, render the player normally
        if abs(self.dashing) <= 50:
            super().draw(surface, offset)

    def jump(self):
        """Make the player jump"""

        # If player is wall sliding
        if self.wall_slide:
            # If player is facing right and is trying to move left
            if self.flip_animation and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                # Push him a little higher
                self.velocity[1] = -2.5
                # Set air time
                self.air_time = 5
                # Decrease the jumps
                self.jumps = max(0, self.jumps - 1)
                return True

            # If player is facing left and is trying to move right
            elif not self.flip_animation and self.last_movement[0] > 0:
                # Push the player off the wall
                self.velocity[0] = -3.5
                # Push him a little higher
                self.velocity[1] = -2.5
                # Set air time
                self.air_time = 5

                # Decrease the jumps
                self.jumps = max(0, self.jumps - 1)
                return True

        # If player has jumps left
        elif self.jumps:
            # Set the velocity to up by -3
            self.velocity[1] = -3
            # Decrease jumps count
            self.jumps -= 1
            # Set the air time to amount needed for jump action
            self.air_time = 5
            return True

    def dash(self):
        """Make player dash"""
        # If player isn't dashing
        if not self.dashing:
            # If dashing to the left, set the dashing direction to left (minus) and time to 60
            if self.flip_animation:
                self.dashing = -60
            # If dashing to the right, set the dashing direction to right and time to 60
            else:
                self.dashing = 60


class Enemy(PhysicsEntity):
    """Enemy entity"""
    def __init__(self, game, pos, size):
        """Initialize the enemy"""
        super().__init__(game, "enemy", pos, size)
        # Walk timer
        self.walking = 0

    def update(self, tile_map, movement=(0, 0)):
        """Update position of the enemy"""
        # If enemy is walking, continue walking in the right direction
        if self.walking:
            # If the next tile is solid, move forward
            if tile_map.solid_check((self.rect().centerx + (-7 if self.flip_animation else 7),
                                     self.pos[1] + 23)):
                # If there is a wall, change direction
                if self.collisions["Right"] or self.collisions["Left"]:
                    self.flip_animation = not self.flip_animation
                # If not, move forward
                else:
                    movement = (movement[0] - 0.5 if self.flip_animation else 0.5, movement[1])
            # If there is an edge, change the direction
            else:
                self.flip_animation = not self.flip_animation

            # Decrease the timer
            self.walking = max(0, self.walking - 1)

            if not self.walking:
                pass

        # If enemy isn't walking, move every 100 frames for a random time
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        super().update(tile_map, movement)

    def draw(self, surface, offset=(0, 0)):
        """Draw the enemy"""
        super().draw(surface, offset)

        # If the enemy is facing left, flip the gun too, place it in the correct placement
        if self.flip_animation:
            pos_x = self.rect().centerx - 4 - self.game.assets["gun"].get_width() - offset[0]
            pos_y = self.rect().centerx - 4 - self.game.assets["gun"].get_width() - offset[1]
            surface.blit(pygame.transform.flip(self.game.assets["gun"], True, False),
                         (pos_x, pos_y))
        # Else just place it correctly
        else:
            surface.blit(self.game.assets["gun"], (self.rect().centerx + 4 - offset[0],
                                                   self.rect().centery - offset[1]))
