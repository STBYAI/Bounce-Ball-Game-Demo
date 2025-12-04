import pygame
import sys
from game_logic import GameLogic
from game_renderer import GameRenderer

class BounceBallGame:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        
        # 游戏设置
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        
        # 创建窗口
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("弹力球游戏")
        
        # 时钟，控制帧率
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.game_mode = "free"  # 自由模式
        self.game_over = False
        self.score = 0
        
        # 初始化逻辑类和渲染类
        self.game_logic = GameLogic(self.WIDTH, self.HEIGHT)
        self.game_renderer = GameRenderer(self.screen)
        
        # 字体
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_mode = "free"
                        self.game_over = False
                        self.score = 0
                        self.game_logic.reset_ball()
                    elif event.key == pygame.K_2:
                        self.game_mode = "gravity"
                        self.game_over = False
                        self.score = 0
                        self.game_logic.reset_ball()
            
            if not self.game_over:
                # 获取鼠标位置
                mouse_pos = pygame.mouse.get_pos()
                
                # 更新游戏逻辑
                if self.game_mode == "free":
                    self.game_logic.update_free_mode(mouse_pos)
                elif self.game_mode == "gravity":
                    self.game_over = self.game_logic.update_gravity_mode(mouse_pos)
                    if self.game_logic.ball_hit:
                        self.score += 10
                        self.game_logic.ball_hit = False
            
            # 渲染游戏
            self.game_renderer.render(self.game_logic.ball_pos, self.game_logic.mouse_line, self.game_mode, self.score, self.game_over)
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = BounceBallGame()
    game.run()