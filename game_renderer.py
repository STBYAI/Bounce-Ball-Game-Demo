import pygame
import math

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.line_length = 100

    def draw_ball(self, ball):
        pygame.draw.circle(self.screen, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)

    def draw_mouse_paddle(self, mouse_pos, ball_pos):
        mx, my = mouse_pos
        bx, by = ball_pos

        # Calculate angle towards ball
        dx = bx - mx
        dy = by - my
        angle = math.atan2(dy, dx)

        # Calculate line endpoints
        line_x = mx + math.cos(angle) * self.line_length
        line_y = my + math.sin(angle) * self.line_length

        # Draw the line (mouse paddle)
        pygame.draw.line(self.screen, (255, 255, 255), (mx, my), (int(line_x), int(line_y)), 5)

    def draw_mode_selector(self, current_mode):
        # Draw mode selection buttons
        free_rect = pygame.Rect(20, 20, 120, 40)
        gravity_rect = pygame.Rect(150, 20, 120, 40)

        pygame.draw.rect(self.screen, (100, 100, 100), free_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), gravity_rect)

        if current_mode == "free":
            pygame.draw.rect(self.screen, (0, 255, 0), free_rect, 3)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), gravity_rect, 3)

        font = pygame.font.Font(None, 30)
        free_text = font.render("自由模式", True, (255, 255, 255))
        gravity_text = font.render("重力模式", True, (255, 255, 255))

        self.screen.blit(free_text, (30, 30))
        self.screen.blit(gravity_text, (160, 30))

    def draw_score(self, score):
        font = pygame.font.Font(None, 40)
        text = font.render(f"分数: {score}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width - 200, 20))

    def draw_game_over(self, score):
        # Draw semi-transparent background
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))

        font = pygame.font.Font(None, 60)
        game_over_text = font.render("游戏结束", True, (255, 0, 0))
        score_text = font.render(f"最终分数: {score}", True, (255, 255, 255))

        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        # Draw restart button
        restart_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2 + 120, 160, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), restart_rect)

        restart_font = pygame.font.Font(None, 40)
        restart_text = restart_font.render("重新开始", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        self.screen.blit(restart_text, restart_text_rect)

    def clear_screen(self):
        self.screen.fill((0, 0, 0))
