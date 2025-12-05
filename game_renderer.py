import pygame
import math
import os

class GameRenderer:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 尝试加载系统中文字体
        self.font = self.load_chinese_font(36)
        self.large_font = self.load_chinese_font(72)

    def draw_ball(self, ball):
        pygame.draw.circle(
            self.screen,
            ball['color'],
            (int(ball['x']), int(ball['y'])),
            ball['radius']
        )
        # 绘制球的高光效果
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (int(ball['x'] - ball['radius'] * 0.3), int(ball['y'] - ball['radius'] * 0.3)),
            int(ball['radius'] * 0.3)
        )

    def draw_paddle(self, paddle):
        # 计算球拍的四个端点
        angle = paddle['angle']
        half_length = paddle['length'] / 2
        x1 = paddle['x'] + half_length * math.cos(angle)
        y1 = paddle['y'] + half_length * math.sin(angle)
        x2 = paddle['x'] - half_length * math.cos(angle)
        y2 = paddle['y'] - half_length * math.sin(angle)

        # 绘制球拍
        pygame.draw.line(
            self.screen,
            paddle['color'],
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            paddle['width']
        )
        # 绘制球拍端点
        pygame.draw.circle(
            self.screen,
            (255, 0, 0),
            (int(x1), int(y1)),
            3
        )
        pygame.draw.circle(
            self.screen,
            (255, 0, 0),
            (int(x2), int(y2)),
            3
        )

    def draw_score(self, score):
        text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw_mode(self, mode):
        mode_text = "自由模式" if mode == "free" else "重力模式"
        text = self.font.render(mode_text, True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width - text.get_width() - 10, 10))

    def draw_game_over(self, score):
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 绘制游戏结束文本
        game_over_text = self.large_font.render("游戏结束", True, (255, 0, 0))
        score_text = self.font.render(f"最终得分: {score}", True, (255, 255, 255))
        restart_text = self.font.render("按空格键重新开始", True, (255, 255, 255))

        # 居中显示
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def load_chinese_font(self, size):
        # 尝试加载系统中文字体
        font_paths = [
            # Windows 系统字体
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/arial.ttf",
            # Linux 系统字体
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            # macOS 系统字体
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
        
        # 如果没有找到中文字体，使用默认字体
        return pygame.font.Font(None, size)
    
    def draw_start_menu(self):
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 绘制标题
        title_text = self.large_font.render("弹力球游戏", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # 绘制模式选择文本
        mode_text = self.font.render("选择游戏模式:", True, (255, 255, 255))
        mode_rect = mode_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
        self.screen.blit(mode_text, mode_rect)

        # 绘制自由模式按钮
        free_mode_text = self.font.render("1 - 自由模式", True, (255, 255, 255))
        free_mode_rect = free_mode_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        self.screen.blit(free_mode_text, free_mode_rect)

        # 绘制重力模式按钮
        gravity_mode_text = self.font.render("2 - 重力模式", True, (255, 255, 255))
        gravity_mode_rect = gravity_mode_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
        self.screen.blit(gravity_mode_text, gravity_mode_rect)

    def render(self, game_state, show_start_menu=False):
        # 清空屏幕
        self.screen.fill((0, 0, 0))

        if show_start_menu:
            self.draw_start_menu()
        else:
            # 绘制游戏元素
            self.draw_ball(game_state['ball'])
            self.draw_paddle(game_state['paddle'])
            self.draw_score(game_state['score'])
            self.draw_mode(game_state['mode'])

            # 如果游戏结束，绘制游戏结束界面
            if game_state['game_over']:
                self.draw_game_over(game_state['score'])

        # 更新屏幕
        pygame.display.flip()