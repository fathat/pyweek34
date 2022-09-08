import projectile
import objects

class rocket_launcher:
    def __init__(self, app, space):
        self.app = app
        self.space = space
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((0,-3))
            objects.objects.append(projectile.missile(self.app, self.space, "models/missile.stl", firespot, body.angle, 1000))


class machine_gun:
    def __init__(self, app, space):
        self.app = app
        self.space = space
        self.fire_rate = 0.1
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((4,0))
            objects.objects.append(projectile.bullet(self.app, self.space, "models/bullet.stl", firespot, body.angle, 1000))