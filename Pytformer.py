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
from src.Spark import Spark


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
        # Render help display with background
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        # Surface without background
        self.display_2 = pygame.Surface((320, 240))
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

        sound_path = "../dependencies/sounds/"

        # Sound effects
        self.sound_effects = {
            "jump": pygame.mixer.Sound(os.path.join(self.utilities.BASE_PATH, sound_path + "jump.flac")),
            "dash": pygame.mixer.Sound(os.path.join(self.utilities.BASE_PATH, sound_path + "dash.wav")),
            "hit": pygame.mixer.Sound(os.path.join(self.utilities.BASE_PATH, sound_path + "hit.mp3")),
            "shoot": pygame.mixer.Sound(os.path.join(self.utilities.BASE_PATH, sound_path + "shoot.mp3")),
            "ambience": pygame.mixer.Sound(os.path.join(self.utilities.BASE_PATH, sound_path + "ambience.mp3"))
        }

        # Adjust volumes
        self.sound_effects["jump"].set_volume(0.8)
        self.sound_effects["dash"].set_volume(0.9)
        self.sound_effects["hit"].set_volume(0.9)
        self.sound_effects["shoot"].set_volume(0.5)
        self.sound_effects["ambience"].set_volume(0.2)

        # Create player
        self.player = Player(self, (100, 100), (8, 15))
        # Clouds
        self.clouds = Clouds(self.assets["clouds"])

        # Create tile map
        self.tile_map = TileMap(self)

        # Current level
        self.level = 0
        # Load it
        self._load_level(self.level)

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

            # Update the music
            self._update_music()

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
            if self.player.jump():
                self.sound_effects["jump"].play()
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
        # Fill the outline display
        self.display.fill((0, 0, 0, 0))

        # Draw the clouds and sky
        self.display_2.blit(self.assets["background"], (0, 0))
        self.clouds.draw(self.display_2)

        # Draw the tile map
        self.tile_map.draw(self.display, self.camera.scroll)

        # Draw the enemies
        self._draw_enemies()

        # Draw the player if he exists
        if not self.death:
            self.player.draw(self.display, self.camera.scroll)

        # Draw and update particles
        self._draw_particles()

        # Draw projectiles
        self._draw_projectiles()

        # Draw and update sparks
        self._draw_sparks()

        # Create a mask
        display_mask = pygame.mask.from_surface(self.display)
        display_silhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(display_silhouette, offset)

        # Draw the transition if needed
        self._draw_transition()

        self.display_2.blit(self.display, (0, 0))

        # Blit the rendering surface onto the main one, scale it
        self.surface.blit(
            pygame.transform.scale(self.display_2, self.surface.get_size()), self.camera.screen_shake_offset)

        # Update the display surface
        pygame.display.update()

    def _update_music(self):
        """Update the music"""
        # Load and update the music and loop it
        pygame.mixer.music.load(os.path.join(self.utilities.BASE_PATH,
                                             "../dependencies/sounds/music/basic.wav"))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        # Load and update the ambience sounds, loop it
        # self.sound_effects["ambience"].play(-1)

    def _update_pos(self):
        """Update positions of things"""
        # Update level transition
        self._update_transition()

        # Update camera scroll
        self.camera.update_scroll(self.display)

        # Spawn leafs
        self._spawn_leafs()

        # Update the player
        self._update_player()

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
        # Set the leaf spawners
        self._set_leaf_spawners()

        # Enemies
        self.enemies = []

        # Set up entity spawners
        self._set_entity_spawners()

        # Death count
        self.death = 0

        # Level transition
        self.transition = -30

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
                # Create sparks
                for spark_num in range(4):
                    self.sparks.append(Spark(projectile[0],
                                             random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                             2 + random.random()))

            # If projectile is in the world for around 6 seconds (360 frames), remove it
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)

            # If player isn't dashing, handle collision with projectile
            elif abs(self.player.dashing) < 50:
                # If player is hit, handle it
                if self.player.rect().collidepoint(projectile[0]):
                    # Remove the projectile
                    self.projectiles.remove(projectile)
                    # Increase death count
                    self.death += 1
                    # Play the death sound effect
                    self.sound_effects["hit"].play()
                    # Increase screen shake
                    self.camera.screen_shake = max(16, self.camera.screen_shake)

                    # Create sparks and particles in-place of player
                    for particle_num in range(25):
                        angle = random.random() * math.pi * 2
                        # Create spark with calculate angle and a random speed
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))

                        # Calculate particle variables
                        speed = random.random() * 5
                        velocity = [math.cos(angle + math.pi) * speed * 0.5,
                                    math.sin(angle + math.pi) * speed * 0.5]
                        # Create particles with random speed and calculated velocity
                        self.particles.append(Particle(self, "normal", self.player.rect().center,
                                                       velocity, random.randint(0, 7)))

    def _spawn_leafs(self):
        """Spawn leafs at random frames, positions and intervals"""
        for leaf in self.leaf_spawners:
            if random.random() * 49999 < leaf.width * leaf.height:
                pos = (leaf.x + random.random() * leaf.width, leaf.y + random.random() * leaf.height)
                self.particles.append(Particle(self, "leaf", pos,
                                               [-0.1, 0.3], random.randint(0, 20)))

    def _set_leaf_spawners(self):
        """Set the leaf spawners"""
        # Go through each tree in the map
        for tree in self.tile_map.extract([("big_decorations", 1)], True):
            # Calculate the spawner location based off tree
            leaf_spawner = pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            # Add it to the list
            self.leaf_spawners.append(leaf_spawner)

    def _set_entity_spawners(self):
        """Set the entity spawners"""
        for spawner in self.tile_map.extract([("spawners", 0), ("spawners", 1)], False):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                # Reset the air time on death
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (8, 18)))

    def _update_player(self):
        if self.death:
            self.death += 1
            # Make the transition effect
            if self.death >= 10:
                self.transition = min(30, self.transition + 1)
            if self.death > 40:
                self._load_level(self.level)

        if not self.death:
            self.player.update(self.tile_map, (self.movement[1] - self.movement[0], 0))

    def _draw_enemies(self):
        """Draw the enemies"""
        # Go through every enemy alive
        for enemy in self.enemies.copy():
            # Update the enemy, return is it killed
            kill = enemy.update(self.tile_map, (0, 0))
            # Draw it
            enemy.draw(self.display, self.camera.scroll)
            # If it is killed, remove it from the list
            if kill:
                self.enemies.remove(enemy)

    def _update_transition(self):
        """Update the level transition"""
        # If there are no more enemies left, increase the transition
        if not len(self.enemies):
            self.transition += 1
            # If transition is past 30, load new level
            if self.transition > 30:
                # Limit the levels to the amount that exists
                self.level = min(self.level + 1, len(os.listdir(os.path.join(self.utilities.BASE_PATH,
                                                                             "../dependencies/data"))) - 1)
                self._load_level(self.level)
        # If transition is less than 0 (at the beginning), then increase it to show more of the map
        if self.transition < 0:
            self.transition += 1

    def _draw_transition(self):
        """Draw the level transition"""
        # If transition is needed, draw one
        if self.transition:
            # Create special surface for it
            transition_surface = pygame.Surface(self.display.get_size())
            # Draw a circle based off transition value (times 8, because of surface size)
            pygame.draw.circle(transition_surface, (255, 255, 255), (self.display.get_width() // 2,
                               self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
            # Change color key (invisibility)
            transition_surface.set_colorkey((255, 255, 255))
            # Finally, draw the transition
            self.display.blit(transition_surface, (0, 0))


# Only run the game with this file
if __name__ == "__main__":
    # Create the game instance and run it
    game = Pytformer()
    game.run()
