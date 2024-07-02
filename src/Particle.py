class Particle:
    """A simple particle"""
    def __init__(self, game, particle_type, pos, velocity=[0, 0], frame=0):
        """Initialize particle"""
        # Game reference
        self.game = game
        # Particle type
        self.type = particle_type

        # Position variables
        self.pos = list(pos)
        self.velocity = list(velocity)
        # Animation variables
        self.animation = self.game.assets["particles"][self.type].copy()
        self.animation.frame = frame

    def update(self):
        """Update particle frame and position"""
        end = False
        # If animation ends, set the flag to True
        if self.animation.done:
            end = True

        # Update position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        # Update animation
        self.animation.update()
        # Return if the animation is done
        return end

    def draw(self, surface, offset=(0, 0)):
        """Draw the particle"""
        image = self.animation.get_frame_image()
        surface.blit(image, (self.pos[0] - offset[0] - image.get_width() // 2,
                             self.pos[1] - offset[1] - image.get_height() // 2))
