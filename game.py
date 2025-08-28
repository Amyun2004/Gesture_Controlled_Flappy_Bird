import pygame
import sys
import random
import cv2
from bird import Bird
from pipe import Pipe
# NEW: Import the Gesture enum from the other file.
from gesture_detector import Gesture

class Game:
    """The main class for the Flappy Bird game logic and rendering."""
    def __init__(self, gesture_detector):
        # Game constants
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 740
        self.GRAVITY = 1.5
        self.FLAP_STRENGTH = -11
        self.PIPE_VELOCITY = -6
        self.PIPE_GAP = 150
        self.PIPE_WIDTH = 80
        # NEW: A downward force for the open palm gesture.
        self.DIVE_STRENGTH = 3
        
        # Variables for controlling game speed increase
        self.speed_increase_interval = 5
        self.current_pipe_velocity = self.PIPE_VELOCITY
        
        # Setup display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        
        self.load_assets()
        
        self.gesture_detector = gesture_detector
        self.reset_game()
        
    def load_assets(self):
        """Loads all game images and fonts."""
        try:
            self.bg_image = pygame.image.load("flappybirdbg.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            bird_image_orig = pygame.image.load("flappybird.png").convert_alpha()
            self.bird_image = pygame.transform.scale(bird_image_orig, (34*1.5, 24*1.5))
            self.top_pipe_original = pygame.image.load("toppipe.png").convert_alpha()
            self.bottom_pipe_original = pygame.image.load("bottompipe.png").convert_alpha()
            self.font = pygame.font.Font(None, 48)
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            sys.exit()
            
    def reset_game(self):
        """Resets the game to its initial state."""
        self.bird = Bird(self.bird_image, self.SCREEN_WIDTH / 4, self.SCREEN_HEIGHT / 2)
        self.pipes = []
        self.score = 0
        self.game_started = False
        self.game_over = False
        self.current_pipe_velocity = self.PIPE_VELOCITY
        # NEW: Track the last gesture to detect changes (e.g., from palm to fist).
        self.last_gesture = Gesture.NONE
        pygame.time.set_timer(pygame.USEREVENT, 2500)

    def run(self):
        """The main game loop."""
        running = True
        while running:
            # MODIFIED: Get the gesture state, not just a boolean.
            gesture, camera_frame = self.gesture_detector.process_frame()
            if camera_frame is not None:
                cv2.imshow("Gesture Control", camera_frame)
                cv2.waitKey(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT and self.game_started and not self.game_over:
                    self.generate_pipe_pair()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.handle_key_flap()

            # MODIFIED: Handle gestures every frame.
            self.handle_gesture_input(gesture)
            
            self.update_game_state()
            self.draw_elements()
            
            self.clock.tick(60)
            
        self.cleanup()

    def handle_key_flap(self):
        """Handles a flap input from the keyboard."""
        if not self.game_started:
            self.game_started = True
        if self.game_over:
            self.reset_game()
        else:
            self.bird.flap(self.FLAP_STRENGTH)

    # NEW: A dedicated method to handle the new gesture logic.
    def handle_gesture_input(self, gesture):
        """Handles bird movement based on the detected gesture."""
        if self.game_over:
            # If the game is over, a fist will restart it.
            if gesture == Gesture.FIST and self.last_gesture != Gesture.FIST:
                self.reset_game()
        elif not self.game_started and gesture == Gesture.FIST:
            # Start the game on the first fist.
            self.game_started = True
            self.bird.flap(self.FLAP_STRENGTH)
        else:
            # Flap only on the transition from not-a-fist to a-fist.
            if gesture == Gesture.FIST and self.last_gesture != Gesture.FIST:
                self.bird.flap(self.FLAP_STRENGTH)
            # If the palm is open, make the bird dive.
            elif gesture == Gesture.PALM:
                self.bird.velocity = self.DIVE_STRENGTH

        # Update the last gesture state for the next frame.
        self.last_gesture = gesture

    def update_game_state(self):
        """Updates positions, checks for collisions, and manages score."""
        if not self.game_started or self.game_over:
            return

        self.bird.update(self.GRAVITY)
        if self.bird.rect.top <= 0:
            self.bird.rect.top = 0
            self.bird.velocity = 0

        for pipe in self.pipes:
            pipe.update(self.current_pipe_velocity)
            if not pipe.passed and pipe.rect.centerx < self.bird.rect.left:
                pipe.passed = True
                if pipe.rect.bottom > self.SCREEN_HEIGHT / 2:
                     self.score += 1
                     if self.score % self.speed_increase_interval == 0:
                         self.current_pipe_velocity -= 0.5

        self.pipes = [p for p in self.pipes if p.rect.right > 0]
        self.check_collisions()

    def check_collisions(self):
        """Checks for bird collisions with pipes or the ground."""
        if self.bird.rect.bottom >= self.SCREEN_HEIGHT:
            self.game_over = True
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over = True
                
    def generate_pipe_pair(self):
        min_height = 100
        max_height = self.SCREEN_HEIGHT - self.PIPE_GAP - min_height
        top_pipe_height = random.randint(min_height, max_height)
        bottom_pipe_y_start = top_pipe_height + self.PIPE_GAP
        bottom_pipe_height = self.SCREEN_HEIGHT - bottom_pipe_y_start
        
        scaled_top_pipe = pygame.transform.scale(self.top_pipe_original, (self.PIPE_WIDTH, top_pipe_height))
        scaled_bottom_pipe = pygame.transform.scale(self.bottom_pipe_original, (self.PIPE_WIDTH, bottom_pipe_height))

        self.pipes.append(Pipe(scaled_top_pipe, self.SCREEN_WIDTH, top_pipe_height, is_bottom=False))
        self.pipes.append(Pipe(scaled_bottom_pipe, self.SCREEN_WIDTH, bottom_pipe_y_start, is_bottom=True))

    def draw_elements(self):
        self.screen.blit(self.bg_image, (0, 0))
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (20, 20))
        if self.game_over:
            self.draw_game_over()
        pygame.display.update()

    def draw_game_over(self):
        over_font = pygame.font.Font(None, 64)
        over_surf = over_font.render("Game Over", True, (255, 0, 0))
        over_rect = over_surf.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 50))
        restart_surf = self.font.render("Fist to Restart", True, (255, 255, 0))
        restart_rect = restart_surf.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 20))
        self.screen.blit(over_surf, over_rect)
        self.screen.blit(restart_surf, restart_rect)

    def cleanup(self):
        self.gesture_detector.cleanup()
        pygame.quit()
        sys.exit()