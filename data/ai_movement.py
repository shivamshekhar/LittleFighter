def move_enemies(player,enemy):
    if enemy.rect.left > player.rect.right:
        enemy.direction = -1
        enemy.movement[0] = enemy.direction*enemy.walk_speed

    if enemy.rect.right < player.rect.left:
        enemy.direction = 1
        enemy.movement[0] = enemy.direction*enemy.walk_speed

    if enemy.rect.centery > player.rect.centery:
        enemy.movement[1] = -1*enemy.walk_speed

    if enemy.rect.centery < player.rect.centery:
        enemy.movement[1] = enemy.walk_speed
