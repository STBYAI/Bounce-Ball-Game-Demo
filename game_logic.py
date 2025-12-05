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

        # 检查球与水平线的碰撞
        self.check_horizontal_line_collision()
        
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

        # Calculate the angle that makes the line horizontal when mouse is below ball
        # We want the line to be perpendicular to the line connecting mouse and ball
        dx = ball_x - mx
        dy = ball_y - my
        
        # The angle of the line connecting mouse and ball
        angle_to_ball = math.atan2(dy, dx)
        
        # The angle for the paddle line (perpendicular to angle_to_ball)
        paddle_angle = angle_to_ball - math.pi / 2

        # Calculate line endpoints - the line extends equally in both directions perpendicular to mouse-ball line
        line_x1 = mx + math.cos(paddle_angle) * (line_length / 2)
        line_y1 = my + math.sin(paddle_angle) * (line_length / 2)
        line_x2 = mx - math.cos(paddle_angle) * (line_length / 2)
        line_y2 = my - math.sin(paddle_angle) * (line_length / 2)

        # Check if ball is close to the line
        dist_sq = self.distance_to_line_sq(ball_x, ball_y, line_x1, line_y1, line_x2, line_y2)
        if dist_sq <= self.ball.radius ** 2:
            # Calculate collision normal (perpendicular to line, pointing away from mouse to ball direction)
            # The normal should be in the direction from mouse to ball
            normal_x = math.cos(angle_to_ball)
            normal_y = math.sin(angle_to_ball)

            # Calculate reflection vector
            dot = self.ball.vx * normal_x + self.ball.vy * normal_y
            self.ball.vx -= 2 * dot * normal_x
            self.ball.vy -= 2 * dot * normal_y

            # Add some extra velocity
            self.ball.vx += normal_x * 8
            self.ball.vy += normal_y * 8

            # Prevent ball from sticking to the paddle by adjusting its position
            overlap = self.ball.radius - math.sqrt(dist_sq)
            self.ball.x += normal_x * overlap
            self.ball.y += normal_y * overlap

            if self.mode == "gravity":
                self.score += 10

    def check_horizontal_line_collision(self):
        # 检查球与屏幕中线（水平线）的碰撞
        line_y = self.screen_height // 2
        
        # 球的底部或顶部是否接触到水平线
        if (self.ball.y - self.ball.radius <= line_y <= self.ball.y + self.ball.radius):
            # 计算碰撞点的x坐标范围
            if (self.ball.x >= 0 and self.ball.x <= self.screen_width):
                # 反弹：反转y方向速度
                self.ball.vy = -self.ball.vy
                
                # 添加一些额外的向上速度
                self.ball.vy += -5 if self.ball.vy > 0 else 5
                
                # 调整球的位置，防止卡在水平线里
                if self.ball.y < line_y:
                    self.ball.y = line_y - self.ball.radius - 1
                else:
                    self.ball.y = line_y + self.ball.radius + 1

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
