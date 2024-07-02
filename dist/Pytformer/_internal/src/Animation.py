class Animation:
    """Class to manage animations"""
    def __init__(self, images, duration=8, loop=True):
        """Initialize the animation"""
        self.images = images
        self.duration = duration
        self.loop = loop

        self.end = False
        self.frame = 0

    def update(self):
        """Update the frames of animation"""
        # Loop the animation if needed
        if self.loop:
            self.frame = (self.frame + 1) % (self.duration * len(self.images))

        # Move to the next frame without looping
        else:
            next_frame = self.frame + 1
            end_frame = self.duration * len(self.images) - 1
            # Make sure that the next frame is valid
            if next_frame <= end_frame:
                self.frame = next_frame
            else:
                self.frame = end_frame
            # If this was the last frame, end the animation
            if self.frame >= self.duration * len(self.images) - 1:
                self.end = True

    def get_frame_image(self):
        """Get the current frame image"""
        return self.images[int(self.frame / self.duration)]

    def copy_animation(self):
        """Get copy of this animation"""
        return Animation(self.images, self.duration, self.loop)
