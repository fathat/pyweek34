import masks
def pickup_humanoid(arbiter, space, data):
    arbiter.shapes[0].data.pickup(arbiter.shapes[1].data)
    return True

def inflict_damage(arbiter, space, data):
    arbiter.shapes[0].data.hurt(arbiter.shapes[1].data)
    return True

def init(space):
    h = space.add_collision_handler(masks.CATEGORY_PLAYER, masks.CATEGORY_HUMANOID)
    h.pre_solve = pickup_humanoid

    h = space.add_collision_handler(masks.CATEGORY_HUMANOID, masks.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_HUMANOID, masks.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PLAYER, masks.CATEGORY_ENEMY_PROJECTILE)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_ENEMY, masks.CATEGORY_PLAYER_PROJECTILE)
    h.pre_solve = inflict_damage
