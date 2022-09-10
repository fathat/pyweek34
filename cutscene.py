from direct.gui.OnscreenImage import OnscreenImage

class CutScene:
    def __init__(self, app, file, snd):
        self.app = app
        self.counter = 0
        self.img = OnscreenImage(image=file)
        self.img.reparentTo(app.render2d)
        self.show_hud = False
        self.cutscene_snd = snd

    def update(self, dt):
        if self.counter < 0.15:
            self.counter += dt
        elif self.app.input.action:
            return True

        return False

    def destroy(self):
        self.img.destroy()
