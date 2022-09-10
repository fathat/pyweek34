import projectile
import utils


class RocketLauncher:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate
        self.snd = scene.app.loader.loadSfx("sound/521377__jarusca__rocket-launch.mp3")

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, shooter, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = shooter.body.local_to_world((4 * direction.value, 0))
            self.snd.play()
            self.scene.objects.append(
                projectile.Missile(
                    shooter, self.scene, "models/missile.stl", firespot, shooter.body.angle, 1000 * direction.value
                )
            )


class MachineGun:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 0.1
        self.fire_timer = self.fire_rate
        self.snd = scene.app.loader.loadSfx("sound/177912__medetix__pc-quick-lazer.wav")

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, shooter, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = shooter.body.local_to_world((4 * direction.value,0))
            self.snd.play()
            self.scene.objects.append(
                projectile.Bullet(
                    shooter, self.scene, "models/bullet.stl", firespot, shooter.body.angle, 1000 * direction.value
                )
            )


class AlienMachineGun:
    def __init__(self, scene):
        self.scene = scene
        self.fire_rate = 1.0
        self.fire_timer = self.fire_rate
        self.snd = scene.app.loader.loadSfx("sound/177912__medetix__pc-quick-lazer.wav")

    def update(self, dt: float):
        if self.fire_timer < self.fire_rate:
            self.fire_timer += dt

    def fire(self, shooter, direction: utils.Direction):
        if self.fire_timer >= self.fire_rate:
            self.fire_timer = 0.0
            firespot = shooter.body.local_to_world((5 * direction.value,0))
            self.snd.play()
            self.scene.objects.append(
                projectile.Bullet(
                    shooter, self.scene, "models/bullet.stl", firespot, shooter.body.angle, 1000 * direction.value
                )
            )