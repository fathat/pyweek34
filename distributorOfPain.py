import masks


def collide_wall(arbiter, space, data):
    arbiter.shapes[0].data.collision(arbiter.shapes[1].data)
    return True


def inflict_damage(arbiter, space, data):
    arbiter.shapes[0].data.collision(arbiter.shapes[1].data)
    return False


def init(space):
    h = space.add_collision_handler(masks.CATEGORY_PLAYER, masks.CATEGORY_WALL)
    h.pre_solve = collide_wall

    h = space.add_collision_handler(masks.CATEGORY_PLAYER, masks.CATEGORY_HUMANOID)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_HUMANOID)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_PLAYER)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_ENEMY)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_WALL)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_ENEMY)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_PROJECTILE, masks.CATEGORY_CONVOY)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_CONVOY, masks.CATEGORY_HUMANOID)
    h.pre_solve = inflict_damage

    h = space.add_collision_handler(masks.CATEGORY_CONVOY, masks.CATEGORY_ENEMY)
    h.pre_solve = inflict_damage
