import random
import math

from src.config import Config
from src.behaviors import BehaviorType
from src.behaviors import AmoebotState

class Amoebot():
    def __init__(self, triangle_map: 'TriangleMap',  row: int, col:int):
        self.EYE_ON = True
        self.behavior: 'BehaviorType' = BehaviorType.RANDOM
        self.state: 'AmoebotState' = AmoebotState.ACTIVE
        self.intelligent_behavior = None 
        self.heading = 0
        self.target = (0,0)
        self.triangle_map = triangle_map
        self.row = row
        self.col = col
        self.from_pos = (self.row, self.col)
        self.to_pos = (self.row, self.col)
        self.triangle_map.occupy(*self.to_pos)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.connected_bots = set()
        self.phase = "idle"
        self.progress = 0.0
        self.idle_timer = 0

    def set_behavior(self, behavior: 'BehaviorType'):
        self.behavior = behavior

    def set_state(self, new_state: AmoebotState):
        self.state = new_state

        if new_state == AmoebotState.INACTIVE:
            self.set_behavior(BehaviorType.STAY)

        elif new_state == AmoebotState.PASSIVE:
            self.set_behavior(BehaviorType.STAY)

        elif new_state == AmoebotState.ONE_STEP:
            self.set_behavior(BehaviorType.TO_HEADING)
            if Config.Scene.jump_pos:
                self.idle_timer = Config.Amoebot.IDLE_DELAY

        elif new_state == AmoebotState.ACTIVE:
            self.set_behavior(BehaviorType.RANDOM)

    def set_intelligent_behavior(self, behavior_fn: callable):
        self.behavior = BehaviorType.INTELLIGENT
        self.intelligent_behavior = behavior_fn

    def connect(self, bot: 'Amoebot'):
        if bot is self:
            return
        self.connected_bots.add(bot)
        bot.connected_bots.add(self)

    def move(self, heading: int):
        if self.state == AmoebotState.ACTIVE:
            return
        self.heading = heading
        self.set_state(AmoebotState.ONE_STEP)

    def update_connected(self, visited=None):
        if visited is None:
            visited = set()

        if self in visited:
            return
        visited.add(self)

        for bot in self.connected_bots:
            if bot not in visited:
                bot.move(self.heading)
                bot.update_connected(visited)

    def _target_select(self):
        neighbors = self.triangle_map.get_neighbors(self.row, self.col)
        free_neighbors = [n for n in neighbors if not self.triangle_map.is_occupied(*n)]
        if not free_neighbors:
            return False

        if self.behavior == BehaviorType.STAY:
            return False

        elif self.behavior == BehaviorType.RANDOM:
            self.target = random.choice(free_neighbors)

        elif self.behavior == BehaviorType.TO_HEADING:
            target = self.triangle_map.get_valid_target_position(self.row, self.col, self.heading)
            if target:
                self.target = target
            else:
                return False

        elif self.behavior == BehaviorType.INTELLIGENT:
            if self.intelligent_behavior:
                self.intelligent_behavior(self)
                if (not self.triangle_map.is_valid(*self.target)) or self.triangle_map.is_occupied(*self.target):
                    return False
            else:
                return False
        return True

    def set_heading(self, heading:int):
        self.heading = heading

    def stop(self):
        self.set_behavior(BehaviorType.STAY)

    def update(self):
        did_step = False
        if self.phase == "expansion":
            self.update_expansion()
        elif self.phase == "contraction":
            if self.update_contraction():  # true ha most lépett
                did_step = True
        elif self.phase == "idle":
            self.update_idle()
        return did_step

    def update_idle(self):
        self.triangle_map.occupy(*self.to_pos)

        if self.state in {AmoebotState.ACTIVE, AmoebotState.ONE_STEP}:
            self.idle_timer += 1
            if self.idle_timer >= Config.Amoebot.IDLE_DELAY:
                if self._target_select():
                    self.from_pos = (self.row, self.col)
                    self.triangle_map.release(*self.from_pos)
                    self.to_pos = self.target
                    self.triangle_map.occupy(*self.to_pos)
                    self.phase = "expansion"
                    self.progress = 0.0
                    self.idle_timer = 0
                    self.update_connected()

    def update_expansion(self):
        self.progress += Config.Amoebot.SPEED
        if self.progress >= 1.0:
            self.progress = 0.0
            self.phase = "contraction"

            p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
            p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]

            dist = math.dist(p1, p2)
            offset = Config.Amoebot.CIRCLE_SIZE / dist
            t = 1.0 * (1 + offset)

            self.contraction_f1 = (
                p1[0] + (p2[0] - p1[0]) * t,
                p1[1] + (p2[1] - p1[1]) * t
            )

    def update_contraction(self):
        self.progress += Config.Amoebot.SPEED
        if self.progress >= 1.0:
            self.row, self.col = self.to_pos
            self.from_pos = self.to_pos
            self.phase = "idle"
            self.progress = 0.0
            self.idle_timer = 0
            if self.state == AmoebotState.ONE_STEP:
                self.set_state(AmoebotState.PASSIVE)
            return True  # => most lépett
        return False

    def draw(self, drawer):
        p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
        p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]

        if self.phase == "idle":
            self.draw_idle(p2, drawer)
        elif self.phase == "expansion":
            self.draw_expansion(p1, p2, drawer)
        elif self.phase == "contraction":
            self.draw_contraction(p1, p2, drawer)
        else:
            drawer.draw_circle(self.color, p1, Config.Amoebot.CIRCLE_SIZE)

    def draw_idle(self, pos, drawer):
        drawer.draw_circle(self.color, pos, Config.Amoebot.CIRCLE_SIZE)
        if self.EYE_ON:
            self.draw_eye(pos, pos, drawer)

    def draw_expansion(self, p1, p2, drawer):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        offset = Config.Amoebot.CIRCLE_SIZE / dist

        f1_start = (p1[0] + dx * offset, p1[1] + dy * offset)
        f1_end = (p1[0] + dx * (1 + offset), p1[1] + dy * (1 + offset))
        f1 = (
            f1_start[0] + (f1_end[0] - f1_start[0]) * self.progress,
            f1_start[1] + (f1_end[1] - f1_start[1]) * self.progress
        )
        f2 = (p1[0] - dx * offset, p1[1] - dy * offset)
        self.contraction_f1 = f1_end

        drawer.draw_ellipse(f1, f2, self.color)
        if self.EYE_ON:
            self.draw_eye(f1, f2, drawer)

    def draw_contraction(self, p1, p2, drawer):
        dist = math.dist(p1, p2)
        offset = Config.Amoebot.CIRCLE_SIZE / dist
        f1 = self.contraction_f1
        t = self.progress * (1 - offset)
        f2 = (
            p1[0] + (p2[0] - p1[0]) * t,
            p1[1] + (p2[1] - p1[1]) * t
        )

        drawer.draw_ellipse(f1, f2, self.color)
        if self.EYE_ON:
            self.draw_eye(f1, f2, drawer)

    def draw_eye(self, f1, f2, drawer):
        eye_x = f1[0] + (f2[0] - f1[0]) * 0.1
        eye_y = f1[1] + (f2[1] - f1[1]) * 0.1
        drawer.draw_circle(Config.Amoebot.EYE_COLOR, (eye_x, eye_y), Config.Amoebot.EYE_SIZE)