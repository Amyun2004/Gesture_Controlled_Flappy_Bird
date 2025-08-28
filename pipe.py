import pygame

class Pipe:
    """Represents a single pipe (top or bottom) in the game."""
    def __init__(self, image, x, y, is_bottom):
        self.image = image
        self.rect = self.image.get_rect()
        # Position the pipe correctly based on whether it's top or bottom
        if is_bottom:
            self.rect.topleft = (x, y)
        else:
            self.rect.bottomleft = (x, y)
            
        self.passed = False

    def draw(self, screen):
        """Draws the pipe on the screen."""
        screen.blit(self.image, self.rect)

    def update(self, velocity):
        """Moves the pipe to the left."""
        self.rect.x += velocity