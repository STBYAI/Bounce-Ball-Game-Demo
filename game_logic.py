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
        line_length = 80
        
        # 计算鼠标到球的角度
        dx = self.ball_pos[0] - mouse_pos[0]
        dy = self.ball_pos[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        
        # 计算横线的两个端点，让横线接触面积大的地方朝向球
        # 横线垂直于鼠标到球的方向
        perp_angle = angle + math.pi / 2
        
        # 计算横线的两个端点
        start_x = mouse_pos[0] + (line_length / 2) * math.cos(perp_angle)
        start_y = mouse_pos[1] + (line_length / 2) * math.sin(perp_angle)
        end_x = mouse_pos[0] - (line_length / 2) * math.cos(perp_angle)
        end_y = mouse_pos[1] - (line_length / 2) * math.sin(perp_angle)
        
        # 更新鼠标线
        self.mouse_line = [start_x, start_y, end_x, end_y]
        
    def check_ball_mouse_collision(self):
        # 检查球是否与鼠标线碰撞
        line_start = (self.mouse_line[0], self.mouse_line[1])
        line_end = (self.mouse_line[2], self.mouse_line[3])
        ball_pos = (self.ball_pos[0], self.ball_pos[1])
        
        # 计算点到线段的距离
        distance = self.point_to_line_distance(ball_pos, line_start, line_end)
        
        # 如果距离小于球的半径，说明碰撞
        # 同时检查球的运动方向，确保只在球靠近线段时才触发碰撞
        # 计算球的运动方向向量
        if self.ball_speed[0] != 0 or self.ball_speed[1] != 0:
            # 计算线段的方向向量
            line_dx = line_end[0] - line_start[0]
            line_dy = line_end[1] - line_start[1]
            
            # 计算线段的法向量（垂直于线段）
            normal_dx = -line_dy
            normal_dy = line_dx
            
            # 归一化法向量
            normal_length = math.hypot(normal_dx, normal_dy)
            if normal_length > 0:
                normal_dx /= normal_length
                normal_dy /= normal_length
            
            # 计算球的速度向量与法向量的点积
            dot_product = self.ball_speed[0] * normal_dx + self.ball_speed[1] * normal_dy
            
            # 如果点积为正，说明球正在靠近线段
            if dot_product > 0:
                return distance < self.ball_radius
        
        # 如果球静止或远离线段，也进行碰撞检测
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
        
        # 计算球到线段的最近点
        line_start = (self.mouse_line[0], self.mouse_line[1])
        line_end = (self.mouse_line[2], self.mouse_line[3])
        ball_pos = (self.ball_pos[0], self.ball_pos[1])
        
        # 计算最近点
        px, py = ball_pos
        x1, y1 = line_start
        x2, y2 = line_end
        
        # 线段的向量
        line_dx = x2 - x1
        line_dy = y2 - y1
        
        # 计算点到线段的投影
        t = ((px - x1) * line_dx + (py - y1) * line_dy) / (line_dx * line_dx + line_dy * line_dy)
        t = max(0, min(1, t))
        
        # 最近点
        closest_x = x1 + t * line_dx
        closest_y = y1 + t * line_dy
        
        # 将球移动到线的另一侧，避免穿模
        push_distance = self.ball_radius - math.hypot(px - closest_x, py - closest_y)
        if push_distance > 0:
            self.ball_pos[0] += (closest_x - px) * (push_distance / self.ball_radius)
            self.ball_pos[1] += (closest_y - py) * (push_distance / self.ball_radius)
        
        # 计算球的速度向量
        vx = self.ball_speed[0]
        vy = self.ball_speed[1]
        
        # 如果球初始速度为0，给一个初始速度
        if vx == 0 and vy == 0:
            # 计算从鼠标到球的方向
            mouse_pos = ((self.mouse_line[0] + self.mouse_line[2]) / 2, (self.mouse_line[1] + self.mouse_line[3]) / 2)
            dx_ball = self.ball_pos[0] - mouse_pos[0]
            dy_ball = self.ball_pos[1] - mouse_pos[1]
            ball_dist = math.hypot(dx_ball, dy_ball)
            if ball_dist > 0:
                vx = (dx_ball / ball_dist) * 8
                vy = (dy_ball / ball_dist) * 8
        
        # 计算反射向量
        dot_product = vx * nx + vy * ny
        new_vx = vx - 2 * dot_product * nx
        new_vy = vy - 2 * dot_product * ny
        
        # 增加一些速度，让球弹得更远
        speed_multiplier = 1.2
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