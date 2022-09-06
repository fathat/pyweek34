
upPressed = False
leftPressed = False
rightPressed = False


def throttle() -> float:
    """
    :return: returns a value between 0.0 and 1.0 (1.0 is full throttle)
    """
    return 1.0 if upPressed else 0.0


def pitch_axis() -> float:
    """
    :return: returns a value between -1.0 and 1.0 describing how much pitch is being applied
    """
    if leftPressed and rightPressed: return 0.0
    if leftPressed: return -1.0
    if rightPressed: return 1.0
    return 0.0


def on_throttle(down):
    global upPressed
    upPressed = down


def on_pitch_left(down):
    global leftPressed
    leftPressed = down


def on_pitch_right(down):
    global rightPressed
    rightPressed = down


def init(base):
    base.accept('w-up', on_throttle, [False])
    base.accept('w', on_throttle, [True])
    base.accept('a-up', on_pitch_left, [False])
    base.accept('a', on_pitch_left, [True])
    base.accept('d-up', on_pitch_right, [False])
    base.accept('d', on_pitch_right, [True])