import utils

def pickup_humanoid(arbiter, space, data):
    arbiter.shapes[0].data.pickup(arbiter.shapes[1].data)
    return True

def inflict_damage(arbiter, space, data):
    arbiter.shapes[0].data.hurt(arbiter.shapes[1].data)
    return True

def init(space):
    h = space.add_collision_handler(utils.CATEGORY_PLAYER, utils.CATEGORY_HUMANOID)
    h.pre_solve = pickup_humanoid

    h = space.add_collision_handler(utils.CATEGORY_HUMANOID, utils.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(utils.CATEGORY_HUMANOID, utils.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(utils.CATEGORY_PLAYER, utils.CATEGORY_ENEMY_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(utils.CATEGORY_ENEMY, utils.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage
