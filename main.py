import pygame
import cv2
from game import Game
from gesture_detector import GestureDetector

def main():
    """
    Initializes the game and gesture detector, then runs the main game loop.
    """
    pygame.init()
    
    # Create instances of the core components
    gesture_detector = GestureDetector()
    flappy_bird_game = Game(gesture_detector)
    
    # Start the game
    flappy_bird_game.run()

if __name__ == "__main__":
    main()
