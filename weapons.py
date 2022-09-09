import projectile
import utils


class RocketLauncher:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((4 * direction.value, 0))
            self.scene.objects.append(
                projectile.Missile(
                    self.scene, "models/missile.stl", firespot, body.angle, 1000 * direction.value
                )
            )


class MachineGun:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 0.1
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((4 * direction.value,0))
            self.scene.objects.append(
                projectile.Bullet(
                    self.scene, "models/bullet.stl", firespot, body.angle, 1000 * direction.value
                )
            )


class AlienMachineGun:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, body, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = body.local_to_world((5 * direction.value,0))
            self.scene.objects.append(
                projectile.Bullet(
                    self.scene, "models/bullet.stl", firespot, body.angle, 1000 * direction.value
                )
            )