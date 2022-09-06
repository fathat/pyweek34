
upPressed = False
downPressed = False
pitch_ccw_pressed = False
pitch_cw_pressed = False

face_left_pressed = False
face_right_pressed = False

def is_face_left_pressed() -> bool: return face_left_pressed
def is_face_right_pressed() -> bool: return face_right_pressed

def throttle() -> float:
    """
    :return: returns a value between 0.0 and 1.0 (1.0 is full throttle)
    """
    if upPressed and downPressed: return 0.0
    if downPressed: return -1.0
    if upPressed: return 1.0
    return 0.0


def pitch_axis() -> float:
    """
    :return: returns a value between -1.0 and 1.0 describing how much pitch is being applied
    """
    if pitch_ccw_pressed and pitch_cw_pressed: return 0.0
    if pitch_ccw_pressed: return -1.0
    if pitch_cw_pressed: return 1.0
    return 0.0


def on_throttle(down):
    global upPressed
    upPressed = down

def on_dethrottle(down):
    global downPressed
    downPressed = down


def on_pitch_ccw(down):
    global pitch_ccw_pressed
    pitch_ccw_pressed = down


def on_pitch_cw(down):
    global pitch_cw_pressed
    pitch_cw_pressed = down


def on_face_left(down):
    global face_left_pressed
    face_left_pressed = down


def on_face_right(down):
    global face_right_pressed
    face_right_pressed = down


def init(app):
    app.accept('w-up', on_throttle, [False])
    app.accept('w', on_throttle, [True])
    app.accept('s-up', on_dethrottle, [False])
    app.accept('s', on_dethrottle, [True])
    app.accept('a-up', on_pitch_ccw, [False])
    app.accept('a', on_pitch_ccw, [True])
    app.accept('d-up', on_pitch_cw, [False])
    app.accept('d', on_pitch_cw, [True])
    app.accept('arrow_left-up', on_face_left, [False])
    app.accept('arrow_left', on_face_left, [True])
    app.accept('arrow_right-up', on_face_right, [False])
    app.accept('arrow_right', on_face_right, [True])