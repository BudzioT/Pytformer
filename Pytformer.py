import math
import sys
import os
import random

import pygame

from src.Entities import Player, Enemy
from src.Utilities import Utilities
from src.TileMap import TileMap
from src.Camera import Camera
from src.Clouds import Clouds
from src.Animation import Animation
from src.Particle import Particle


class Pytformer:
    """Pytformer - a Python platformer"""
    def __init__(self):
        """Initialize the game"""
        # Initialize pygame
        pygame.init()

        # Set caption
        pygame.display.set_caption("Pytformer")

        # Game surface
        self.surface = pygame.display.set_mode((640, 480))
        # Render help display
        self.display = pygame.Surface((320, 240))
        # Game utilities
        self.utilities = Utilities()

        # Movement of player
        self.movement = [False, False]

        # Assets of the game
        self.assets = {
            # Entities
            "player": self.utilities.load_image("entities/player.png"),
            # Tiles
            "grass": self.utilities.load_images("tiles/grass"),
            "cobblestone": self.utilities.load_images("tiles/cobblestone"),
            # Others
            "decorations": self.utilities.load_images("tiles/decorations"),
            "big_decorations": self.utilities.load_images("tiles/big_decorations"),
            "background": self.utilities.load_image("sky/background.png"),
            "clouds": self.utilities.load_images("sky/clouds/"),
            "gun": self.utilities.load_image("weapon/gun.png"),
            "bullet": self.utilities.load_image("weapon/bullet.png"),
            # Player animations
            "player_animations": {
                "jump": Animation(self.utilities.load_images("entities/player/jump"), 5),
                "idle": Animation(self.utilities.load_images("entities/player/idle"), 30),
                "run": Animation(self.utilities.load_images("entities/player/run"), 7),
                "slide": Animation(self.utilities.load_images("entities/player/slide")),
                "wall_slide": Animation(self.utilities.load_images("entities/player/wall_slide"))
            },
            # Enemy animations
            "enemy_animations": {
                "idle": Animation(self.utilities.load_images("entities/enemy/idle"), 30),
                "run": Animation(self.utilities.load_images("entities/enemy/run"), 7)
            },
            # Particles
            "particles": {
                "normal": Animation(self.utilities.load_images("particles/normal"), 20, False),
                "leaf": Animation(self.utilities.load_images("particles/leaf"), 20, False)
            }
        }

        # Create player
        self.player = Player(self, (100, 100), (8, 17))
        # Clouds
        self.clouds = Clouds(self.assets["clouds"])

        # Create tile map
        self.tile_map = TileMap(self)
        # Load it
        self._load_level(0)

        # Camera
        self.camera = Camera(self)

        # FPS timer
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the game"""
        # Game loop
        while True:
            # Handle the events
            self._get_events()

            # Update the surface
            self._update_surface()

            # Update positions
            self._update_pos()

            # Run the game in 60 FPS
            self.timer.tick(60)

    def _get_events(self):
        """Get the input events"""
        # Go through each event
        for event in pygame.event.get():
            # If event is quit request, quit the game
            if event.type == pygame.QUIT:
                # Free the pygame resources
                pygame.quit()
                sys.exit()
            # Handle keydown events
            if event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            # Handle keyup events
            if event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

    def _handle_keydown_events(self, event):
        """Handle keydown events"""
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # Movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = True
            self.player.last_movement = [-1, self.player.last_movement[1]]
        # Movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = True
            self.player.last_movement = [-1, self.player.last_movement[1]]
        # Jump
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.jump()
        # Dash
        if event.key == pygame.K_x or event.key == pygame.K_l:
            self.player.dash()

    def _handle_keyup_events(self, event):
        """Handle keyup events"""
        # End movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.movement[0] = False
        # End movement to the right
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.movement[1] = False

    def _update_surface(self):
        """Update the surface"""
        # Draw the clouds and sky
        self.display.blit(self.assets["background"], (0, 0))
        self.clouds.draw(self.display)

        # Draw the tile map
        self.tile_map.draw(self.display, self.camera.scroll)

        for enemy in self.enemies.copy():
            enemy.update(self.tile_map, (0, 0))
            enemy.draw(self.display, self.camera.scroll)

        # Draw the player
        self.player.draw(self.display, self.camera.scroll)

        # Draw and update particles
        self._draw_particles()

        # Draw and update sparks
        self._draw_sparks()

        # Blit the rendering surface onto the main one, scale it
        self.surface.blit(
            pygame.transform.scale(self.display, self.surface.get_size()), (0, 0))

        # Update the display surface
        pygame.display.update()

    def _update_pos(self):
        """Update positions of things"""
        # Update camera scroll
        self.camera.update_scroll(self.display)

        # Spawn leafs
        self._spawn_leafs()

        # Update the player
        self.player.update(self.tile_map,
                           (self.movement[1] - self.movement[0], 0))

        # Update clouds
        self.clouds.update()

    def _load_level(self, level_id):
        """Load level with given id"""
        self.tile_map.load(os.path.join(self.utilities.BASE_PATH, "../dependencies/data/level")
                           + str(level_id) + ".json")
        # Particles
        self.particles = []
        # Projectiles
        self.projectiles = []
        # Sparks
        self.sparks = []

        # Leaf particle spawners - the trees
        self.leaf_spawners = []
        # Go through each tree in the map
        for tree in self.tile_map.extract([("big_decorations", 1)], True):
            # Calculate the spawner location based off tree
            leaf_spawner = pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            # Add it to the list
            self.leaf_spawners.append(leaf_spawner)

        # Enemies
        self.enemies = []

        # Set up entity spawners
        for spawner in self.tile_map.extract([("spawners", 0), ("spawners", 1)], False):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (8, 15)))

    def _draw_particles(self):
        """Update and draw particles"""
        # Go through each particle that is active
        for particle in self.particles.copy():
            # Update the particle, store if it was the last frame
            end = particle.update()
            # Draw it
            particle.draw(self.display, self.camera.scroll)
            # If it was leaf, update its position, so it seems like it floats
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.03) * 0.3
            # If it was the last frame and particle is not active, delete it
            if end:
                self.particles.remove(particle)

    def _draw_sparks(self):
        """Update and draw sparks"""
        # Go through every spark
        for spark in self.sparks.copy():
            # Update it, save if this was the last frame
            end = spark.update()
            # Draw it
            spark.draw(self.display, self.camera.scroll)
            # If this was the last frame, remove the spark
            if end:
                self.sparks.remove(spark)

    def _draw_projectiles(self):
        """Draw the projectiles"""
        # Go through every projectile (format: [[x, y], direction, timer])
        for projectile in self.projectiles.copy():
            # Add direction to the position - update position
            projectile[0][0] += projectile[1]
            # Increase the timer
            projectile[2] += 1

            image = self.assets["bullet"]
            # Display the projectile in correct place in the world
            self.display.blit(image, (projectile[0][0] - image.get_width() / 2 - self.camera.scroll[0],
                                      projectile[0][1] - image.get_height() / 2 - self.camera.scroll[1]))
            # If projectile hit the solid surface, remove it
            if self.tile_map.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
            # If projectile is in the world for around 6 seconds (360 frames), remove it
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            # If player isn't dashing, handle collision with projectile
            elif abs(self.player.dashing) < 50:
                # If player is hit, handle it
                if self.player.rect().collidepoint(projectile[0]):
                    # Remove the projectile
                    self.projectiles.remove(projectile)

    def _spawn_leafs(self):
        """Spawn leafs at random frames, positions and intervals"""
        for leaf in self.leaf_spawners:
            if random.random() * 49999 < leaf.width * leaf.height:
                pos = (leaf.x + random.random() * leaf.width, leaf.y + random.random() * leaf.height)
                self.particles.append(Particle(self, "leaf", pos,
                                               [-0.1, 0.3], random.randint(0, 20)))


# Only run the game with this file
if __name__ == "__main__":
    # Create the game instance and run it
    game = Pytformer()
    game.run()
