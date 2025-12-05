import pygame

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        # 使用支持中文的字体
        try:
            self.font = pygame.font.Font("msyh.ttc", 36)
        except:
            try:
                self.font = pygame.font.Font("simhei.ttf", 36)
            except:
                self.font = pygame.font.Font(None, 36)
        
    def render(self, ball_pos, mouse_line, game_mode, score, game_over):
        # 填充背景
        self.screen.fill((0, 0, 0))
        
        # 绘制球
        pygame.draw.circle(self.screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), 20)
        
        # 绘制鼠标线
        pygame.draw.line(self.screen, (255, 255, 0), (mouse_line[0], mouse_line[1]), (mouse_line[2], mouse_line[3]), 3)
        
        # 绘制游戏模式信息
        mode_text = self.font.render(f"模式: {game_mode} (1-自由模式, 2-重力模式)", True, (255, 255, 255))
        self.screen.blit(mode_text, (10, 10))
        
        # 绘制分数
        score_text = self.font.render(f"分数: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 50))
        
        # 如果游戏结束，显示游戏结束信息
        if game_over:
            game_over_text = self.font.render("游戏结束! 按1或2重新开始", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"最终分数: {score}", True, (255, 255, 255))
            final_score_rect = final_score_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
            self.screen.blit(final_score_text, final_score_rect)