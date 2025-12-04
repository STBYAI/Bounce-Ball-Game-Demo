import math
import pygame

class GameLogic:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.ball_radius = 20
        self.ball_speed = [0, 0]
        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]
        self.gravity = 0.5
        self.mouse_line = [0, 0, 0, 0]  # 鼠标线的起点和终点
        self.ball_hit = False
        
    def reset_ball(self):
        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]
        self.ball_speed = [0, 0]
        self.ball_hit = False
        
    def update_free_mode(self, mouse_pos):
        # 更新鼠标线位置和角度
        self.update_mouse_line(mouse_pos)
        
        # 球的运动
        self.ball_pos[0] += self.ball_speed[0]
        self.ball_pos[1] += self.ball_speed[1]
        
        # 碰撞检测：球碰到鼠标线
        if self.check_ball_mouse_collision():
            self.bounce_off_mouse()
        
        # 碰撞检测：球碰到屏幕边缘
        self.check_wall_collision_free_mode()
        
    def update_gravity_mode(self, mouse_pos):
        # 更新鼠标线位置和角度
        self.update_mouse_line(mouse_pos)
        
        # 应用重力
        self.ball_speed[1] += self.gravity
        
        # 球的运动
        self.ball_pos[0] += self.ball_speed[0]
        self.ball_pos[1] += self.ball_speed[1]
        
        # 碰撞检测：球碰到鼠标线
        if self.check_ball_mouse_collision():
            self.bounce_off_mouse()
            self.ball_hit = True
        
        # 碰撞检测：球碰到屏幕边缘
        self.check_wall_collision_gravity_mode()
        
        # 检查球是否落地（游戏结束）
        if self.ball_pos[1] + self.ball_radius >= self.HEIGHT:
            return True
        
        return False
        
    def update_mouse_line(self, mouse_pos):
        # 鼠标线长度
        line_length = 50
        
        # 计算鼠标到球的角度
        dx = self.ball_pos[0] - mouse_pos[0]
        dy = self.ball_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        
        # 计算鼠标线的终点
        end_x = mouse_pos[0] + line_length * math.cos(angle)
        end_y = mouse_pos[1] + line_length * math.sin(angle)
        
        # 更新鼠标线
        self.mouse_line = [mouse_pos[0], mouse_pos[1], end_x, end_y]
        
    def check_ball_mouse_collision(self):
        # 检查球是否与鼠标线碰撞
        line_start = (self.mouse_line[0], self.mouse_line[1])
        line_end = (self.mouse_line[2], self.mouse_line[3])
        ball_pos = (self.ball_pos[0], self.ball_pos[1])
        
        # 计算点到线段的距离
        distance = self.point_to_line_distance(ball_pos, line_start, line_end)
        
        # 如果距离小于球的半径，说明碰撞
        return distance < self.ball_radius
        
    def point_to_line_distance(self, point, line_start, line_end):
        # 计算点到线段的距离
        px, py = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # 线段的向量
        dx = x2 - x1
        dy = y2 - y1
        
        # 如果线段长度为0，直接返回点到点的距离
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
        
        # 计算点到线段的投影
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        
        # 投影点
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        
        # 计算距离
        return math.hypot(px - proj_x, py - proj_y)
        
    def bounce_off_mouse(self):
        # 计算鼠标线的方向向量
        dx = self.mouse_line[2] - self.mouse_line[0]
        dy = self.mouse_line[3] - self.mouse_line[1]
        
        # 归一化方向向量
        length = math.hypot(dx, dy)
        if length == 0:
            return
        
        nx = dx / length
        ny = dy / length
        
        # 计算球的速度向量
        vx = self.ball_speed[0]
        vy = self.ball_speed[1]
        
        # 计算反射向量
        dot_product = vx * nx + vy * ny
        new_vx = vx - 2 * dot_product * nx
        new_vy = vy - 2 * dot_product * ny
        
        # 增加一些速度，让球弹得更远
        speed_multiplier = 1.5
        self.ball_speed[0] = new_vx * speed_multiplier
        self.ball_speed[1] = new_vy * speed_multiplier
        
    def check_wall_collision_free_mode(self):
        # 自由模式下的墙壁碰撞检测，碰到边缘会减速
        if self.ball_pos[0] - self.ball_radius <= 0:
            self.ball_pos[0] = self.ball_radius
            self.ball_speed[0] = -self.ball_speed[0] * 0.8  # 减速
        elif self.ball_pos[0] + self.ball_radius >= self.WIDTH:
            self.ball_pos[0] = self.WIDTH - self.ball_radius
            self.ball_speed[0] = -self.ball_speed[0] * 0.8  # 减速
        
        if self.ball_pos[1] - self.ball_radius <= 0:
            self.ball_pos[1] = self.ball_radius
            self.ball_speed[1] = -self.ball_speed[1] * 0.8  # 减速
        elif self.ball_pos[1] + self.ball_radius >= self.HEIGHT:
            self.ball_pos[1] = self.HEIGHT - self.ball_radius
            self.ball_speed[1] = -self.ball_speed[1] * 0.8  # 减速
            
    def check_wall_collision_gravity_mode(self):
        # 重力模式下的墙壁碰撞检测，碰到边缘不减速
        if self.ball_pos[0] - self.ball_radius <= 0:
            self.ball_pos[0] = self.ball_radius
            self.ball_speed[0] = -self.ball_speed[0]
        elif self.ball_pos[0] + self.ball_radius >= self.WIDTH:
            self.ball_pos[0] = self.WIDTH - self.ball_radius
            self.ball_speed[0] = -self.ball_speed[0]
        
        if self.ball_pos[1] - self.ball_radius <= 0:
            self.ball_pos[1] = self.ball_radius
            self.ball_speed[1] = -self.ball_speed[1]