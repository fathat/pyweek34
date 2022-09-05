from pyhocon import ConfigFactory

class SceneDefinition:
    scene_cfg = None

    def __init__(self, scene_name):
        self.scene_cfg = ConfigFactory.parse_file("./scenes/" + scene_name + ".config")
