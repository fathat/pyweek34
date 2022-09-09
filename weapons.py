import projectile
import objects
import utils


class RocketLauncher:
    def __init__(self, app, space):
        self.app = app
        self.space = space
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((4 * direction.value, 0))
            objects.objects.append(
                projectile.Missile(
                    self.app, self.space, "models/missile.stl", firespot, body.angle, 1000 * direction.value
                )
            )


class MachineGun:
    def __init__(self, app, space):
        self.app = app
        self.space = space
        self.fire_rate = 0.1
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((4 * direction.value,0))
            objects.objects.append(
                projectile.Bullet(
                    self.app, self.space, "models/bullet.stl", firespot, body.angle, 1000 * direction.value
                )
            )


class AlienMachineGun:
    def __init__(self, app, space):
        self.app = app
        self.space = space
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((5 * direction.value,0))
            objects.objects.append(
                projectile.Bullet(
                    self.app, self.space, "models/bullet.stl", firespot, body.angle, 1000 * direction.value
                )
            )