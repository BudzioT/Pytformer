import random


class Cloud:
    """Cloud that flies through the skies"""
    def __init__(self, pos, image, speed, pos_z):
        self.pos = list(pos)
        self.image = image
        self.speed = speed
        self.pos_z = pos_z

    def update(self):
        """Update cloud position"""
        self.pos[0] += self.speed

    def draw(self, surface, offset=(0, 0)):
        """Draw the cloud and loop it"""
        # Normal draw position
        draw_pos = (self.pos[0] - offset[0] * self.pos_z, self.pos[1] - offset[1] * self.pos_z)
        # Looped position
        loop_pos = (draw_pos[0] %
                    (surface.get_width() + self.image.get_width()) - self.image.get_width(),
                    draw_pos[1] % (surface.get_height() + self.image.get_height())
                    - self.image.get_height())
        surface.blit(self.image, loop_pos)


class Clouds:
    """Group of clouds"""
    def __init__(self, images, count=12):
        """Initialize group of clouds"""
        # Cloud group
        self.clouds = []
        # Count
        self.count = count
        # Images
        self.images = images

        # Create given amount of clouds
        self._create_clouds()

    def _create_clouds(self):
        """Create given amount of clouds"""
        # Create a new random cloud, append it to the group given number of times
        for cloud_num in range(self.count):
            # Position
            random_pos = (random.random() * 99999, random.random() * 99999)
            # Image
            random_image = random.choice(self.images)
            # Speed
            random_speed = random.random() * 0.03 + 0.05
            # Depth
            random_pos_z = random.random() * 0.6 + 0.2
            # New completely random cloud
            new_cloud = Cloud(random_pos, random_image, random_speed, random_pos_z)
            self.clouds.append(new_cloud)

        # Sort the clouds, so the Z position counts
        self.clouds.sort(key=lambda cloud: cloud.pos_z)

    def update(self):
        """Update position of clouds"""
        for cloud in self.clouds:
            cloud.update()

    def draw(self, surface, offset=(0, 0)):
        """Draw the clouds"""
        for cloud in self.clouds:
            cloud.draw(surface, offset)
