from typing import Tuple
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import PointLight, LVector3, LensNode, PerspectiveLens, SamplerState, TextureStage, LQuaternionf, \
    LineSegs, NodePath, Filename
import pymunk
from input import InputManager
from utils import clamp, not_zero, radians_to_degrees, damp, move_towards, slerp, almost_zero, Direction
from masks import CATEGORY_PLAYER, CATEGORY_WALL
import math
import simplepbr
from direct.actor.Actor import Actor
import weapons
import masks
import utils

from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect

class Chopper:
    width: float = 3.2
    hull_top: float = 1.25
    hull_mid: float = -0.25
    hull_floor: float = -1.0

    skid_floor: float = -1.5
    skid_height: float = 0.25

    rotor_floor: float = 1.5
    rotor_height: float = 0.25
    rotor_radius: float = 1.5

    scale: float = 1.0
    direction: Direction = Direction.RIGHT
    scene: "scene.Scene"
    space: pymunk.Space

    def __init__(self, app, scene: "scene.Scene", spawn_point: Tuple[float, float]):
        width, scale = self.width, self.scale
        space = scene.space
        self.spawn_point = spawn_point
        self.scene = scene
        self.space = space
        self.app = app
        self.input = app.input
        self.score = 0
        self.flip_heading_t = 0
        self.flip_heading = False
        self.bodyNode = Actor("art/space-chopper/space-chopper.glb")
        self.bodyNode.reparentTo(app.render)
        self.bodyNode.loop("blade")

        self.bodyNode.setShaderAuto()
        self.bodyNode.setTextureOff(1)
        for material in self.bodyNode.findAllMaterials():
            print(material)

        # self.shadowNode = self.bodyNode.attachNewNode(LensNode('shadowproj'))
        # #lens = PerspectiveLens()
        # lens = PerspectiveLens()
        # lens.setNearFar(1, 5)
        # self.shadowNode.node().setLens(lens)
        # self.shadowNode.node().showFrustum()
        # self.shadowNode.setHpr(0, -90, 0)
        # self.shadowNode.find('frustum').setColor(1, 0, 0, 1)
        # self.shadowNode.reparentTo(self.bodyNode)
        # self.shadowNode.setPos(0, 0, self.height)

        # tex = app.loader.loadTexture('art/space-chopper/shadow.png')
        # tex.setWrapU(SamplerState.WMBorderColor)
        # tex.setWrapV(SamplerState.WMBorderColor)
        # tex.setBorderColor((1, 1, 1, 0))
        # ts = TextureStage('ts')
        # ts.setSort(1)
        # ts.setColor((0.5, 0.5, 0.5, 0.5))
        # ts.setMode(TextureStage.MCombine)
        # ts.setCombineRgb(
        #     TextureStage.CMInterpolate, 
        #     TextureStage.CSTexture, 
        #     TextureStage.COSrcColor,
        #     TextureStage.CSPrevious,
        #     TextureStage.COSrcColor,
        #     TextureStage.CSTexture,
        #     TextureStage.COOneMinusSrcColor
        #     )
        # scene.worldNP.projectTexture(ts, tex, self.shadowNode)

       
        #self.roterNode = base.loader.loadModel("models/Roter.stl")
        #self.roterNode.reparentTo(self.bodyNode)

        self.body = pymunk.Body(5, 100)
        self.body.position = self.spawn_point

        # hull
        hull_vertices = [
            (-width*scale, self.hull_mid*scale), 
            (0, self.hull_floor*scale), 
            (width*scale, self.hull_mid*scale), 
            (0, self.hull_top*scale)
        ]
        hull_shape = pymunk.Poly(self.body, hull_vertices)
        hull_shape.friction = 0.5
        hull_shape.filter = pymunk.ShapeFilter(categories=CATEGORY_PLAYER)
        hull_shape.collision_type = CATEGORY_PLAYER
        hull_shape.data = self
        
        # skids
        skid_vertices = [
            (-width*scale,  self.skid_floor*scale), 
            ( width*scale,  self.skid_floor*scale), 
            ( width*scale,  (self.skid_floor + self.skid_height)*scale),  
            (-width*scale,  (self.skid_floor + self.skid_height)*scale)
        ]
        skid_shape = pymunk.Poly(self.body, skid_vertices)
        skid_shape.friction = 0.5
        skid_shape.filter = pymunk.ShapeFilter(categories=CATEGORY_PLAYER)
        skid_shape.collision_type = CATEGORY_PLAYER
        skid_shape.data = self

        # rotor
        rotor_vertices = [
            (-self.rotor_radius*scale,  self.rotor_floor*scale), 
            ( self.rotor_radius*scale,  self.rotor_floor*scale), 
            ( self.rotor_radius*scale,  (self.rotor_floor + self.rotor_height)*scale),  
            (-self.rotor_radius*scale,  (self.rotor_floor + self.rotor_height)*scale)
        ]
        rotor_shape = pymunk.Poly(self.body, rotor_vertices)
        rotor_shape.friction = 0.5
        rotor_shape.filter = pymunk.ShapeFilter(categories=CATEGORY_PLAYER)
        rotor_shape.collision_type = CATEGORY_PLAYER
        rotor_shape.data = self
        
        space.add(self.body, hull_shape, skid_shape, rotor_shape)

        self.weapons = [weapons.MachineGun(app, space), weapons.RocketLauncher(app, space)]
        
        self.debug_lines = LineSegs()
        self.debug_lines.setColor(1, 0, 0, 1)
        def draw_shape(vertices):
            self.debug_lines.moveTo(vertices[0][0], 0, vertices[0][1])
            for v in vertices[1:]:
                self.debug_lines.drawTo(v[0], 0, v[1])
            self.debug_lines.drawTo(vertices[0][0], 0, vertices[0][1])

        draw_shape(hull_vertices)
        draw_shape(skid_vertices)
        draw_shape(rotor_vertices)

        self.debug_lines.setThickness(4)
        self.debug_line_node = self.debug_lines.create()
        self.debug_line_np = NodePath(self.debug_line_node)
        self.debug_line_np.reparentTo(self.bodyNode)
        self.debug_line_np.setHpr(90, 0, 0)

        self.debug_line_np.hide()

        # self.dust_particles = ParticleEffect()
        # self.dust_particles.loadConfig(Filename("./art/effects/dust.ptf"))
        # self.dust_particles.clearLight()
        # #self.dust_particles.start(scene.app.render)
        # self.dust_particles_active = False
        #
        # self.particles = Particles()
        # self.particles.setFactory("PointParticleFactory")
        # self.particles.setRenderer("SpriteParticleRenderer")
        # self.particles.setEmitter("SphereVolumeEmitter")


    def velocity(self) -> float: return self.body.velocity.length

    def update(self, dt: float):
        im: InputManager = self.input

        # ground_intersection = self.ground_intersection(15)
        # if ground_intersection:
        #     if not self.dust_particles_active:
        #         self.dust_particles = ParticleEffect()
        #         self.dust_particles.loadConfig(Filename("./art/effects/dust.ptf"))
        #         self.dust_particles.start(self.scene.app.render)
        #         self.dust_particles_active = True
        #     self.dust_particles.setPos(ground_intersection.point.x, 0.000, ground_intersection.point.y)
        # else:
        #     if self.dust_particles_active:
        #         self.dust_particles.softStop()
        #     self.dust_particles_active = False

        if not_zero(im.throttle()):
            self.body.apply_force_at_local_point((0, 200 * im.throttle()), (0, 0))

        self.bodyNode.setPlayRate(5.0 + 15 * im.throttle(), "blade")

        if im.is_booster_rocket_pressed():
            self.body.apply_force_at_local_point((self.direction.value * 200, 0), (0, 0))
        
        if im.is_reverse_booster_rocket_pressed():
            self.body.apply_force_at_local_point((-self.direction.value * 200, 0), (0, 0))

        if im.is_face_left_pressed() and self.direction != Direction.LEFT:
            self.direction = Direction.LEFT
            self.flip_heading_t = 0
            self.flip_heading = True
        elif im.is_face_right_pressed() and self.direction != Direction.RIGHT:
            self.direction = Direction.RIGHT
            self.flip_heading_t = 0
            self.flip_heading = True

        self.weapons[im.weapon_selection].update(dt)

        if im.fire_pressed:
            self.weapons[im.weapon_selection].fire(self.body, self.direction)

        if not_zero(im.pitch_axis()):
            self.body.apply_force_at_world_point((10 * im.pitch_axis(), 0), (self.body.position.x, self.body.position.y))
            self.body.apply_force_at_local_point((0, 200 * im.pitch_axis()), (-self.width, 0))
            self.body.apply_force_at_local_point((0, -200 * im.pitch_axis()), (self.width, 0))

        #damping_rate = 1.0 - clamp(self.velocity() / 100, 0, 1)
        #self.body.velocity = damp(self.body.velocity, damping_rate, dt)
        self.body.angular_velocity = damp(self.body.angular_velocity, 0.15, dt)

        self.pos = self.body.position
        rot = self.body.angle

        while rot < 0:
            rot += math.pi * 2
        while rot > math.pi * 2:
            rot -= math.pi * 2

        self.body.angle = rot

        self.bodyNode.setPos(self.pos.x, 0, self.pos.y)

        if self.flip_heading:
            if self.flip_heading_t >= 1.0:
                self.flip_heading_t = 1.0
                self.flip_heading = False

            src_rotation = LQuaternionf()
            src_rotation.setHpr(LVector3(90 * -self.direction.value, radians_to_degrees(rot) * self.direction.value, 0))
            target_rotation = LQuaternionf()
            target_rotation.setHpr(LVector3(90 * self.direction.value, -radians_to_degrees(rot) * self.direction.value, 0))
            self.bodyNode.setQuat(slerp(src_rotation, target_rotation, self.flip_heading_t))
            self.flip_heading_t = move_towards(self.flip_heading_t, 1.0, 5.0, dt)
        else:
            self.bodyNode.setHpr(LVector3(90 * self.direction.value, -radians_to_degrees(rot) * self.direction.value, 0))

    def ground_intersection(self, dist):
        segment_query_info_list = self.space.segment_query((self.body.position.x, self.body.position.y), (self.body.position.x, self.body.position.y - dist), 0.1, pymunk.ShapeFilter(mask=CATEGORY_WALL))
        segment_query_info_list.sort(key=lambda x: x.alpha)
        if len(segment_query_info_list) == 0: return None
        return segment_query_info_list[0]

    def distance_to_ground(self):
        segment_query_info_list = self.space.segment_query((self.body.position.x, self.body.position.y), (self.body.position.x, self.body.position.y - 50), 0.1, pymunk.ShapeFilter(mask=CATEGORY_WALL))
        segment_query_info_list.sort(key=lambda x: x.alpha)
        if len(segment_query_info_list) == 0: return -1
        if almost_zero(segment_query_info_list[0].alpha): return 0
        return (segment_query_info_list[0].point - self.body.position).length

    def collision(self, other):
        if other.shape.collision_type == masks.CATEGORY_HUMANOID:
            other.destroyed = True
            self.score += 1
        elif other.shape.collision_type == masks.CATEGORY_WALL:
            angle = utils.normalizeAngle(self.body.angle, 0.0)
            if abs(angle) > math.pi * 0.66:
                self.body.position = self.spawn_point
                self.body.angle = 0