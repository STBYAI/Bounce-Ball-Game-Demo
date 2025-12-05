import math

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.color = (255, 255, 255)
        self.gravity = 0
        self.bounce_damping = 0.8
        self.edge_damping = 0.9

    def update(self, screen_width, screen_height):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # 边界碰撞检测
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * self.edge_damping
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.vx = -self.vx * self.edge_damping

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy * self.edge_damping
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.vy = -self.vy * self.edge_damping

    def check_paddle_collision(self, paddle):
        # 计算球拍的法线方向（垂直于球拍平面）
        normal_angle = paddle.angle - math.pi / 2
        
        # 计算球到球拍的向量
        dx = self.x - paddle.x
        dy = self.y - paddle.y
        
        # 计算球在法线上的投影
        dot_product = dx * math.cos(normal_angle) + dy * math.sin(normal_angle)
        
        # 如果球在球拍的背面，不发生碰撞
        if dot_product > 0:
            return False
        
        # 计算反弹速度
        # 速度在法线上的分量反转
        normal_vx = math.cos(normal_angle)
        normal_vy = math.sin(normal_angle)
        
        # 计算速度在法线上的分量
        speed_normal = self.vx * normal_vx + self.vy * normal_vy
        
        # 如果球正在远离球拍，不发生碰撞
        if speed_normal > 0:
            return False
        
        # 反转法向速度分量并增加弹力
        # 增加更大的弹力值，使球反弹更高
        self.vx -= 2 * speed_normal * normal_vx * 1.5  # 增加弹力
        self.vy -= 2 * speed_normal * normal_vy * 1.5  # 增加弹力
        
        # 额外增加一些速度，使游戏更有乐趣
        speed = math.hypot(self.vx, self.vy)
        if speed > 0:
            # 增加更大的速度提升
            self.vx = (self.vx / speed) * (speed * 1.3)
            self.vy = (self.vy / speed) * (speed * 1.3)
        
        return True

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.width = 5
        self.angle = 0
        self.color = (255, 255, 255)

    def update(self, ball_x, ball_y):
        # 计算球拍朝向球的角度（让横线平面朝向球，而不是端点朝向球）
        dx = ball_x - self.x
        dy = ball_y - self.y
        # 计算垂直于球方向的角度，这样横线平面朝向球
        self.angle = math.atan2(dy, dx) + math.pi / 2

    def check_ball_collision(self, ball):
        # 计算球拍的两个端点
        angle = self.angle
        half_length = self.length / 2

        x1 = self.x + half_length * math.cos(angle)
        y1 = self.y + half_length * math.sin(angle)
        x2 = self.x - half_length * math.cos(angle)
        y2 = self.y - half_length * math.sin(angle)

        # 计算球到线段的距离
        A = ball.x - x1
        B = ball.y - y1
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

        dx = ball.x - xx
        dy = ball.y - yy
        distance = math.hypot(dx, dy)

        # 检查球是否在线段附近
        if distance < ball.radius:
            # 纠正球的位置，防止穿模
            if distance > 0:
                overlap = ball.radius - distance
                ball.x += (dx / distance) * overlap
                ball.y += (dy / distance) * overlap
            return True
        return False


class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball = Ball(screen_width // 2, screen_height // 2, 15)
        self.paddle = Paddle(screen_width // 2, screen_height // 2)
        self.score = 0
        self.game_over = False
        self.mode = "free"
        self.gravity = 0.5

    def set_mode(self, mode):
        self.mode = mode
        self.reset()
        if mode == "gravity":
            self.ball.gravity = self.gravity
            self.ball.edge_damping = 1.0  # 重力模式下边缘不减速
        else:
            self.ball.gravity = 0
            self.ball.edge_damping = 0.9  # 自由模式下边缘减速
            # 自由模式下给球一个微小的初始速度，防止完全静止
            self.ball.vx = 0.1
            self.ball.vy = 0.1

    def reset(self):
        self.ball.reset(self.screen_width // 2, self.screen_height // 2)
        self.score = 0
        self.game_over = False

    def update(self, mouse_x, mouse_y):
        if self.game_over:
            return

        # 更新球拍位置和角度
        self.paddle.x = mouse_x
        self.paddle.y = mouse_y
        self.paddle.update(self.ball.x, self.ball.y)

        # 更新球
        self.ball.update(self.screen_width, self.screen_height)

        # 检测球拍与球的碰撞
        if self.paddle.check_ball_collision(self.ball):
            # 只需要一个碰撞检测，简化逻辑
            self.ball.check_paddle_collision(self.paddle)
            if self.mode == "gravity":
                self.score += 10

        # 重力模式下检测球是否落地
        if self.mode == "gravity" and self.ball.y + self.ball.radius >= self.screen_height - 10:
            self.game_over = True

    def get_game_state(self):
        return {
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "radius": self.ball.radius,
                "color": self.ball.color
            },
            "paddle": {
                "x": self.paddle.x,
                "y": self.paddle.y,
                "length": self.paddle.length,
                "width": self.paddle.width,
                "angle": self.paddle.angle,
                "color": self.paddle.color
            },
            "score": self.score,
            "game_over": self.game_over,
            "mode": self.mode
        }