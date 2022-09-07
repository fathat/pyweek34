from pyhocon import ConfigFactory

class SceneDefinition:
    scene_cfg = None
    cutscene = False
    spawn_point: list[float] | str = [0, 0]

    def __init__(self, scene_name):
        self.scene_cfg = ConfigFactory.parse_file("./scenes/" + scene_name + "/scene.config")
        self.cutscene = self.scene_cfg.get_bool('cutscene', False)
        self.world_mesh = self.scene_cfg.get_string('world_mesh')
        self.gravity = self.scene_cfg.get_float('gravity')
        self.fog_density = self.scene_cfg.get_float('fog_density')
        self.sun_color = self.scene_cfg.get('sun_color')
        self.background_color = self.scene_cfg.get('background')
        self.spawn_point = self.scene_cfg.get('spawn_point', [0, 0])
