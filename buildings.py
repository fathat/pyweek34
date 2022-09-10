from panda3d.core import NodePath
from typing import Tuple
from scene_definition import BuildingDefinition
from scene_colliders import add_node_path_as_collider


class Building:
    def __init__(self, scene: "scene.Scene", definition: BuildingDefinition):
        self.scene = scene
        self.node_path = scene.app.loader.loadModel(definition.model)
        self.node_path.reparentTo(scene.root)
        self.node_path.setPos(*tuple(definition.pos))
        self.node_path.setHpr(*tuple(definition.hpr))
        self.node_path.setShaderAuto()
        add_node_path_as_collider(self.node_path, self.scene.space, self.scene.collisionDebugNP)


class Helipad(Building):
    def __init__(self, scene: "scene.Scene", definition: BuildingDefinition):
        super().__init__(scene, definition)


def make_building(scene, definition: BuildingDefinition) -> Building:
    if definition.type == 'helipad':
        return Helipad(scene, definition)
    return Building(scene, definition)