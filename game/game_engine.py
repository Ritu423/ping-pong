import pygame
from .paddle import Paddle
from .ball import Ball
import math
import array 

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 10
        self.font = pygame.font.SysFont("Arial", 30)

        # Load sound effects
        self.snd_paddle = self.generate_beep(600, 50)
        self.snd_wall = self.generate_beep(400, 50)
        self.snd_score = self.generate_beep(800, 50)

    def generate_beep(self, freq=440, duration_ms=15, volume=0.3):
        sample_rate = 44100
        n_samples = int(sample_rate * duration_ms / 1000)
        buf = array.array("h", [int(math.sin(2 * math.pi * freq * t / sample_rate) * 32767 * volume) for t in range(n_samples)])
        return pygame.mixer.Sound(buffer=buf)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball (play wall sound if bounces)
        self.ball.move(self.snd_wall)

        # Get current rectangles
        ball_rect = self.ball.rect()
        player_rect = self.player.rect()
        ai_rect = self.ai.rect()

        # Paddle collisions
        if ball_rect.colliderect(player_rect):
            self.ball.x = player_rect.right
            self.ball.velocity_x *= -1
            self.snd_paddle.play()

        elif ball_rect.colliderect(ai_rect):
            self.ball.x = ai_rect.left - self.ball.width
            self.ball.velocity_x *= -1
            self.snd_paddle.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            self.snd_score.play()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()
            self.snd_score.play()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

        # Game Over / Replay
        self.check_game_over(pygame.display.get_surface())



    def check_game_over(self, screen):
        # If someone reaches the winning score
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            # Determine winner
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"

            # Display the winner
            screen.fill((0, 0, 0))
            winner_surface = self.font.render(winner_text, True, WHITE)
            winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 60))
            screen.blit(winner_surface, winner_rect)

            # Display replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]

            for i, text in enumerate(options):
                option_surface = self.font.render(text, True, WHITE)
                option_rect = option_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
                screen.blit(option_surface, option_rect)

            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key == pygame.K_3:
                            self.winning_score = 2  # Best of 3 means first to 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 3  # Best of 5 means first to 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4  # Best of 7 means first to 4
                            waiting = False

            # Reset everything for a new match
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()



    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
