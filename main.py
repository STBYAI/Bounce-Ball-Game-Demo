import pygame
from game_logic import GameLogic
from game_renderer import GameRenderer

class BounceBallGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("弹力球游戏")

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.game_logic = GameLogic(self.screen_width, self.screen_height)
        self.game_renderer = GameRenderer(self.screen)

        self.mouse_pos = (self.screen_width // 2, self.screen_height // 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicking mode buttons
                if event.button == 1:
                    mx, my = event.pos
                    # Free mode button
                    if 20 <= mx <= 140 and 20 <= my <= 60:
                        self.game_logic.set_mode("free")
                    # Gravity mode button
                    elif 150 <= mx <= 270 and 20 <= my <= 60:
                        self.game_logic.set_mode("gravity")
                    # Restart button (only if game over)
                    elif self.game_logic.game_over:
                        if self.screen_width // 2 - 80 <= mx <= self.screen_width // 2 + 80 and \
                           self.screen_height // 2 + 120 <= my <= self.screen_height // 2 + 170:
                            self.game_logic.reset()

        return True

    def update(self):
        self.game_logic.update(self.mouse_pos)
        self.game_logic.check_mouse_collision(self.mouse_pos, self.game_renderer.line_length)

    def render(self):
        self.game_renderer.clear_screen()

        # Draw mode selector
        self.game_renderer.draw_mode_selector(self.game_logic.mode)

        # Draw score (only in gravity mode)
        if self.game_logic.mode == "gravity":
            self.game_renderer.draw_score(self.game_logic.score)

        # Draw ball
        self.game_renderer.draw_ball(self.game_logic.ball)

        # Draw mouse paddle
        self.game_renderer.draw_mouse_paddle(self.mouse_pos, (self.game_logic.ball.x, self.game_logic.ball.y))

        # Draw game over screen if needed
        if self.game_logic.game_over:
            self.game_renderer.draw_game_over(self.game_logic.score)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = BounceBallGame()
    game.run()
