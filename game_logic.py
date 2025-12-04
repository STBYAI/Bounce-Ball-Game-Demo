import math

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.mass = 1.0

class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball = Ball(screen_width // 2, screen_height // 2, 20)
        self.mode = "free"  # "free" or "gravity"
        self.score = 0
        self.game_over = False
        self.gravity = 0.5

    def set_mode(self, mode):
        self.mode = mode
        self.reset()

    def reset(self):
        self.ball = Ball(self.screen_width // 2, self.screen_height // 2, 20)
        self.score = 0
        self.game_over = False

    def update(self, mouse_pos):
        if self.game_over:
            return

        if self.mode == "gravity":
            self.ball.vy += self.gravity

        # Update ball position
        self.ball.x += self.ball.vx
        self.ball.y += self.ball.vy

        # Ball collision with screen edges
        if self.ball.x - self.ball.radius <= 0:
            self.ball.x = self.ball.radius
            self.ball.vx = -self.ball.vx
            if self.mode == "free":
                self.ball.vx *= 0.8
                self.ball.vy *= 0.8
        elif self.ball.x + self.ball.radius >= self.screen_width:
            self.ball.x = self.screen_width - self.ball.radius
            self.ball.vx = -self.ball.vx
            if self.mode == "free":
                self.ball.vx *= 0.8
                self.ball.vy *= 0.8

        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.vy = -self.ball.vy
            if self.mode == "free":
                self.ball.vx *= 0.8
                self.ball.vy *= 0.8
        elif self.ball.y + self.ball.radius >= self.screen_height:
            if self.mode == "gravity":
                self.game_over = True
            else:
                self.ball.y = self.screen_height - self.ball.radius
                self.ball.vy = -self.ball.vy
                self.ball.vx *= 0.8
                self.ball.vy *= 0.8

    def check_mouse_collision(self, mouse_pos, line_length):
        if self.game_over:
            return

        mx, my = mouse_pos
        ball_x, ball_y = self.ball.x, self.ball.y

        # Calculate line angle towards ball
        dx = ball_x - mx
        dy = ball_y - my
        angle = math.atan2(dy, dx)

        # Calculate line endpoints
        line_x = mx + math.cos(angle) * line_length
        line_y = my + math.sin(angle) * line_length

        # Check if ball is close to the line
        dist_sq = self.distance_to_line_sq(ball_x, ball_y, mx, my, line_x, line_y)
        if dist_sq <= self.ball.radius ** 2:
            # Calculate collision normal (perpendicular to line)
            normal_x = -math.sin(angle)
            normal_y = math.cos(angle)

            # Check if normal is pointing towards ball
            dot_product = (ball_x - mx) * normal_x + (ball_y - my) * normal_y
            if dot_product < 0:
                normal_x = -normal_x
                normal_y = -normal_y

            # Calculate reflection vector
            dot = self.ball.vx * normal_x + self.ball.vy * normal_y
            self.ball.vx -= 2 * dot * normal_x
            self.ball.vy -= 2 * dot * normal_y

            # Add some extra velocity
            self.ball.vx += normal_x * 5
            self.ball.vy += normal_y * 5

            if self.mode == "gravity":
                self.score += 10

    def distance_to_line_sq(self, px, py, x1, y1, x2, y2):
        # Calculate squared distance from point (px, py) to line segment (x1,y1)-(x2,y2)
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1

        if len_sq != 0:
            param = dot / len_sq

        if param < 0:
            xx = x1
            yy = y1
        elif param > 1:
            xx = x2
            yy = y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D

        dx = px - xx
        dy = py - yy
        return dx * dx + dy * dy
