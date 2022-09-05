
upPressed = False
leftPressed = False
rightPressed = False

def on_w(down):
    global upPressed
    upPressed = down

def on_a(down):
    global leftPressed
    leftPressed = down

def on_d(down):
    global rightPressed
    rightPressed = down

#def on_r(down):
#    body.apply_force_at_local_point((0,50), (50,0))
#
#def on_f(down):
#    body.apply_force_at_local_point((0,50), (-50,0))

def init(base):
    base.accept('w-up', on_w, [False])
    base.accept('w', on_w, [True])
    base.accept('a-up', on_a, [False])
    base.accept('a', on_a, [True])
    base.accept('d-up', on_d, [False])
    base.accept('d', on_d, [True])
    #base.accept('r-up', on_r, [False])
    #base.accept('f-up', on_f, [False])