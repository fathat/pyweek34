from typing import List, Union
from pyhocon import ConfigFactory
import random

class SceneDefinition:
    scene_cfg = None
    cutscene = False
    texture_hack = False
    spawn_point: Union[List[float], str] = [0, 0]

    def __init__(self, scene_name):
        self.scene_cfg = ConfigFactory.parse_file("./scenes/" + scene_name + "/scene.config")
        self.cutscene = self.scene_cfg.get_bool('cutscene', False)
        self.texture_hack = self.scene_cfg.get_bool('texture_hack', False)
        self.world_mesh = self.scene_cfg.get_string('world_mesh')
        self.gravity = self.scene_cfg.get_float('gravity')
        self.fog_density = self.scene_cfg.get_float('fog_density')
        self.sun_color = self.scene_cfg.get('sun_color')
        self.background_color = self.scene_cfg.get('background')
        self.spawn_point = self.scene_cfg.get('spawn_point', [0, 0])
        self.objective = self.scene_cfg.get_string('objective')
        self.objective_amount = self.scene_cfg.get_float('objective_amount')
        self.convoy_spawn_point = self.scene_cfg.get('convoy_spawn_point', [0, 0])
        self.convoy_goal_point = self.scene_cfg.get('convoy_goal_point', [0, 0])
        self.civilian_models = self.scene_cfg.get('civilian_models')
        self.num_civilians = self.scene_cfg.get_int('num_civilians', 40)

    def random_civ_model(self):
        return random.choice(self.civilian_models)
