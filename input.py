from panda3d.core import InputDevice


class InputManager:

    upPressed = False
    downPressed = False
    pitch_ccw_pressed = False
    pitch_cw_pressed = False

    face_left_pressed = False
    face_right_pressed = False


    def __init__(self, app):

        # check for a gamepad
        self.app = app
        self.gamepad = None

        devices = app.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            print("Found gamepad, connecting...")
            self.connect(devices[0])

        app.accept("connect-device", self.connect)
        app.accept("disconnect-device", self.disconnect)

        app.accept('w-up', self.on_throttle, [False])
        app.accept('w', self.on_throttle, [True])
        app.accept('s-up', self.on_dethrottle, [False])
        app.accept('s', self.on_dethrottle, [True])
        app.accept('a-up', self.on_pitch_ccw, [False])
        app.accept('a', self.on_pitch_ccw, [True])
        app.accept('d-up', self.on_pitch_cw, [False])
        app.accept('d', self.on_pitch_cw, [True])
        app.accept('arrow_left-up', self.on_face_left, [False])
        app.accept('arrow_left', self.on_face_left, [True])
        app.accept('arrow_right-up', self.on_face_right, [False])
        app.accept('arrow_right', self.on_face_right, [True])

    def connect(self, device):
        """Event handler that is called when a device is discovered."""

        # We're only interested if this is a gamepad and we don't have a
        # gamepad yet.
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            print("Found %s" % (device))
            self.gamepad = device

            # Enable this device to ShowBase so that we can receive events.
            # We set up the events with a prefix of "gamepad-".
            self.app.attachInputDevice(device, prefix="gamepad")


    def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.gamepad != device:
            # We don't care since it's not our gamepad.
            return

        # Tell ShowBase that the device is no longer needed.
        print("Disconnected %s" % (device))
        self.app.detachInputDevice(device)
        self.gamepad = None

        # Do we have any other gamepads?  Attach the first other gamepad.
        devices = self.app.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            self.connect(devices[0])

    def is_face_left_pressed(self) -> bool: 
        if self.face_left_pressed:
            return True
        if self.gamepad:
            right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
            return right_x.value < -0.2
        return False

    def is_face_right_pressed(self) -> bool: 
        if self.face_left_pressed:
            return True
        if self.gamepad:
            right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
            return right_x.value > 0.2
        return False

    def throttle(self) -> float:
        """
        :return: returns a value between 0.0 and 1.0 (1.0 is full throttle)
        """
        if self.upPressed and self.downPressed: return 0.0
        if self.downPressed: return -1.0
        if self.upPressed: return 1.0

        if self.gamepad:
            left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
            trigger_l = self.gamepad.findAxis(InputDevice.Axis.left_trigger)
            trigger_r = self.gamepad.findAxis(InputDevice.Axis.right_trigger)
            lift = trigger_r.value - trigger_l.value
            return left_y.value if abs(left_y.value) > abs(lift) else lift

        return 0.0


    def pitch_axis(self) -> float:
        """
        :return: returns a value between -1.0 and 1.0 describing how much pitch is being applied
        """
        if self.pitch_ccw_pressed and self.pitch_cw_pressed: return 0.0
        if self.pitch_ccw_pressed: return -1.0
        if self.pitch_cw_pressed: return 1.0

        if self.gamepad:
            left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
            return left_x.value

        return 0.0


    def on_throttle(self, down):
        self.upPressed = down

    def on_dethrottle(self, down):
        self.downPressed = down


    def on_pitch_ccw(self, down):
        self.pitch_ccw_pressed = down


    def on_pitch_cw(self, down):
        self.pitch_cw_pressed = down


    def on_face_left(self, down):
        self.face_left_pressed = down


    def on_face_right(self, down):
        self.face_right_pressed = down

