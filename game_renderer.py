import pygame
import math

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.line_length = 100
        
        # 尝试加载系统中的中文字体，如果失败则使用默认字体
        self.chinese_font_name = self.find_chinese_font()
        self.fonts = {
            'small': self.get_font(25),
            'medium': self.get_font(30),
            'large': self.get_font(40),
            'xlarge': self.get_font(60),
        }
    
    def find_chinese_font(self):
        # 尝试查找系统中的中文字体
        # Windows系统常见的中文字体
        windows_fonts = [
            'SimHei', 'Microsoft YaHei', 'FangSong', 'KaiTi',
            'SimSun', 'NSimSun', 'SimSun-ExtB'
        ]
        
        # 检查字体是否存在
        for font_name in windows_fonts:
            try:
                # 尝试初始化字体，如果成功则返回字体名称
                font = pygame.font.SysFont(font_name, 30)
                if font: 
                    return font_name
            except:
                continue
        
        # 如果没有找到合适的中文字体，返回None使用默认字体
        return None
    
    def get_font(self, size):
        try:
            if self.chinese_font_name:
                return pygame.font.SysFont(self.chinese_font_name, size)
            else:
                return pygame.font.Font(None, size)
        except:
            # 如果加载失败，使用默认字体
            return pygame.font.Font(None, size)

    def draw_ball(self, ball):
        pygame.draw.circle(self.screen, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)

    def draw_mouse_paddle(self, mouse_pos, ball_pos):
        mx, my = mouse_pos
        bx, by = ball_pos

        # Calculate the angle that makes the line horizontal when mouse is below ball
        # We want the line to be perpendicular to the line connecting mouse and ball
        dx = bx - mx
        dy = by - my
        
        # The angle of the line connecting mouse and ball
        angle_to_ball = math.atan2(dy, dx)
        
        # The angle for the paddle line (perpendicular to angle_to_ball)
        paddle_angle = angle_to_ball - math.pi / 2

        # Calculate line endpoints - the line extends equally in both directions perpendicular to mouse-ball line
        line_x1 = mx + math.cos(paddle_angle) * (self.line_length / 2)
        line_y1 = my + math.sin(paddle_angle) * (self.line_length / 2)
        line_x2 = mx - math.cos(paddle_angle) * (self.line_length / 2)
        line_y2 = my - math.sin(paddle_angle) * (self.line_length / 2)

        # Draw the line (mouse paddle)
        pygame.draw.line(self.screen, (255, 255, 255), (int(line_x1), int(line_y1)), (int(line_x2), int(line_y2)), 5)

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

        font = self.fonts['medium']
        free_text = font.render("自由模式", True, (255, 255, 255))
        gravity_text = font.render("重力模式", True, (255, 255, 255))

        self.screen.blit(free_text, (30, 30))
        self.screen.blit(gravity_text, (160, 30))

    def draw_score(self, score):
        font = self.fonts['large']
        text = font.render(f"分数: {score}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width - 200, 20))

    def draw_game_over(self, score):
        # Draw semi-transparent background
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))

        font = self.fonts['xlarge']
        game_over_text = font.render("游戏结束", True, (255, 0, 0))
        score_text = font.render(f"最终分数: {score}", True, (255, 255, 255))

        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        # Draw restart button
        restart_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2 + 120, 160, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), restart_rect)

        restart_font = self.fonts['large']
        restart_text = restart_font.render("重新开始", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        self.screen.blit(restart_text, restart_text_rect)

    def clear_screen(self):
        self.screen.fill((0, 0, 0))
