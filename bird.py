import pygame

class Bird:
    """Represents the player-controlled bird in the game."""
    def __init__(self, image, x, y):
        self.image = image
        # pygame.Rect is perfect for handling position, size, and collision
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def draw(self, screen):
        """Draws the bird on the screen."""
        screen.blit(self.image, self.rect)

    def update(self, gravity):
        """Updates the bird's vertical position based on gravity."""
        self.velocity += gravity
        self.rect.y += int(self.velocity)

    def flap(self, flap_strength):
        """Applies an upward velocity to the bird."""
        self.velocity = flap_strength