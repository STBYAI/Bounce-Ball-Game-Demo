import pygame
from game_logic import GameLogic
from game_renderer import GameRenderer

class BounceBallGame:
    def __init__(self):
        # 初始化Pygame
        pygame.init()

        # 设置屏幕尺寸
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Bounce Ball Game")

        # 创建游戏逻辑和渲染器
        self.game_logic = GameLogic(self.screen_width, self.screen_height)
        self.game_renderer = GameRenderer(self.screen, self.screen_width, self.screen_height)

        # 游戏状态
        self.running = True
        self.show_start_menu = True
        self.clock = pygame.time.Clock()
        self.fps = 60

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.show_start_menu:
                    # 开始菜单按键处理
                    if event.key == pygame.K_1:
                        self.game_logic.set_mode("free")
                        self.show_start_menu = False
                    elif event.key == pygame.K_2:
                        self.game_logic.set_mode("gravity")
                        self.show_start_menu = False
                else:
                    # 游戏中按键处理
                    if event.key == pygame.K_SPACE and self.game_logic.game_over:
                        self.game_logic.reset()
                    elif event.key == pygame.K_m:
                        # 切换模式
                        current_mode = self.game_logic.mode
                        new_mode = "gravity" if current_mode == "free" else "free"
                        self.game_logic.set_mode(new_mode)

    def run(self):
        while self.running:
            # 处理事件
            self.handle_events()

            if not self.show_start_menu:
                # 获取鼠标位置
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # 更新游戏逻辑
                self.game_logic.update(mouse_x, mouse_y)

            # 获取游戏状态
            game_state = self.game_logic.get_game_state()

            # 渲染游戏
            self.game_renderer.render(game_state, self.show_start_menu)

            # 控制帧率
            self.clock.tick(self.fps)

        # 退出游戏
        pygame.quit()

if __name__ == "__main__":
    game = BounceBallGame()
    game.run()