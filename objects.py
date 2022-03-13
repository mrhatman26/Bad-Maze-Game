import pygame
from pygame.sprite import Sprite
from pathing import check_next_node, path_find, cell_number_calc
import sys
#Player Object:
class Player(Sprite):
    def __init__(self, x, y, node_x, node_y, direction):
        self.node_x = node_x
        self.node_y = node_y
        self.image_right = pygame.image.load("Sprites\\Player\\spr_player_right.png").convert()
        self.image_left = pygame.image.load("Sprites\\Player\\spr_player_left.png").convert()
        self.image_up = pygame.image.load("Sprites\\Player\\spr_player_up.png").convert()
        self.image_down = pygame.image.load("Sprites\\Player\\spr_player_down.png").convert()
        self.image_right = self.image_right.convert_alpha()
        self.image_left = self.image_left.convert_alpha()
        self.image_up = self.image_up.convert_alpha()
        self.image_down = self.image_down.convert_alpha()
        self.rect = pygame.rect.Rect(x, y, 64, 64)
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.move = False
        self.bullet_pos_switch = False
        self.health = 100
        self.recovery_timer = 1000

    def move_player(self, cells, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.direction -= 90
                if self.direction < 0:
                    self.direction = 270
            if event.key == pygame.K_e:
                self.direction += 90
                if self.direction > 270:
                    self.direction = 0
            if event.key == pygame.K_d:
                self.direction = 0
                self.move = check_next_node(self.direction, cells, self.node_x, self.node_y)
            if event.key == pygame.K_w:
                self.direction = 90
                self.move = check_next_node(self.direction, cells, self.node_x, self.node_y)
            if event.key == pygame.K_a:
                self.direction = 180
                self.move = check_next_node(self.direction, cells, self.node_x, self.node_y)
            if event.key == pygame.K_s:
                self.direction = 270
                self.move = check_next_node(self.direction, cells, self.node_x, self.node_y)
            if self.move is True:
                if self.direction == 0:
                    self.rect.x += 100
                    self.node_x += 1
                if self.direction == 90:
                    self.rect.y -= 100
                    self.node_y -= 1
                if self.direction == 180:
                    self.rect.x -= 100
                    self.node_x -= 1
                if self.direction == 270:
                    self.rect.y += 100
                    self.node_y += 1
                self.move = False
        return None

    def shoot_check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.bullet_pos_switch is False:
                    if self.direction == 0:
                        self.bullet_pos_switch = True
                        return (self.rect.x + 30, self.rect.y + 14)
                    if self.direction == 90:
                        self.bullet_pos_switch = True
                        return (self.rect.x + 12, self.rect.y + 1)
                    if self.direction == 180:
                        self.bullet_pos_switch = True
                        return (self.rect.x + 1, self.rect.y + 51)
                    if self.direction == 270:
                        self.bullet_pos_switch = True
                        return (self.rect.x + 47, self.rect.y + 62)
                else:
                    if self.direction == 0:
                        self.bullet_pos_switch = False
                        return (self.rect.x + 62, self.rect.y + 49)
                    if self.direction == 90:
                        self.bullet_pos_switch = False
                        return (self.rect.x + 47, self.rect.y + 1)
                    if self.direction == 180:
                        self.bullet_pos_switch = False
                        return (self.rect.x + 1, self.rect.y + 12)
                    if self.direction == 270:
                        self.bullet_pos_switch = False
                        return (self.rect.x + 12, self.rect.y + 62)
        return None

    def update(self):
        #print("X: " + str(self.rect.x) + "\nY: " + str(self.rect.y))
        if self.health < 100:
            self.recovery_timer -= 1
            if self.recovery_timer < 1:
                self.health += 10
                if self.health > 100:
                    self.health = 100
                self.recovery_timer = 1000

    def draw(self, target, game_over):
        if game_over is True:
            self.image_right.set_alpha(128)
            self.image_left.set_alpha(128)
            self.image_up.set_alpha(128)
            self.image_down.set_alpha(128)
        if self.direction == 0:
            target.blit(self.image_right, (self.rect.x - 32, self.rect.y - 32))
        if self.direction == 90:
            target.blit(self.image_up, (self.rect.x - 32, self.rect.y - 32))
        if self.direction == 180:
            target.blit(self.image_left, (self.rect.x - 32, self.rect.y - 32))
        if self.direction == 270:
            target.blit(self.image_down, (self.rect.x - 32, self.rect.y - 32))
        #pygame.draw.circle(target, (255, 0, 0), (self.rect.x, self.rect.y), 8)
    
class PlayerBullet(Sprite):
    def __init__(self, x, y, node_x, node_y, direction):
        super().__init__()
        self.node_x = node_x
        self.node_y = node_y
        self.image = pygame.image.load("Sprites\\Player\\spr_player_bullet.png").convert()
        self.image = pygame.transform.rotate(self.image, direction)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.node_increase = 0
        self.speed = 5

    def update(self, cells, screen_info):
        if self.direction == 0:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.x += self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_x += 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 90:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.y -= self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_y -= 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 180:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.x -= self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_x -= 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 270:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.y += self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_y += 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.rect.x >= screen_info["width"] or self.rect.x <= 0:
            return True
        if self.rect.y >= screen_info["height"] or self.rect.y <= 0:
            return True
        return False

    def draw(self, target):
        target.blit(self.image, (self.rect.x - 32, self.rect.y - 32))

class Enemy(Sprite):
    def __init__(self, x, y, node_x, node_y, direction):
        super().__init__()
        self.node_x = node_x
        self.node_y = node_y
        self.image_right = pygame.image.load("Sprites\\Enemy\\spr_enemy_right.png").convert()
        self.image_left = pygame.image.load("Sprites\\Enemy\\spr_enemy_left.png").convert()
        self.image_up = pygame.image.load("Sprites\\Enemy\\spr_enemy_up.png").convert()
        self.image_down = pygame.image.load("Sprites\\Enemy\\spr_enemy_down.png").convert()
        self.image_destroyed = pygame.image.load("Sprites\\Enemy\\spr_enemy_destroyed.png").convert()
        self.rect = pygame.rect.Rect(x, y, 64, 64)
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.move = False
        self.path = None
        self.path_find_timer = 1000
        self.path_move_timer = 1200
        self.shoot = False
        self.shoot_timer = 50
        self.despawn_timer = 1000
        self.destroyed = False

    def enemy_move(self, debug):
        if self.destroyed is False:
            self.path_move_timer -= 1
            if self.path_move_timer < 1:
                self.path_move_timer = 500#1200
                if self.path != None:
                    try:
                        if debug is True:
                            print("Path: " + str(self.path))
                        cell = self.path.pop(0)
                        cell = cell.split(",")
                        if debug is True:
                            print("Target Cell: " + str(cell))
                        y = int(cell[0])
                        x = int(cell[1])
                        cell_number = cell_number_calc(y, x, False)
                        if debug is True:
                            print("Target Cell Number: " + str(cell_number))
                        my_cell_number = cell_number_calc(self.node_y, self.node_x, False)
                        if debug is True:
                            print("My node: " + str(self.node_y) + ", " + str(self.node_x))
                            print("My cell number: " + str(my_cell_number) + "\nMy cell + 10: " + str(my_cell_number + 10) + "\nMy cell - 10: " + str(my_cell_number - 10) + "\nMy cell + 1: " + str(my_cell_number + 1) + "\nMy cell - 1: " + str(my_cell_number))
                        if my_cell_number + 10 == cell_number:
                            self.rect.x += 100
                            self.node_x += 1
                            self.direction = 0
                            if debug is True:
                                print("\n\nMOVED SUCCESSFULLY!!!!\n\n")
                        elif my_cell_number - 10 == cell_number:
                            self.rect.x -= 100
                            self.node_x -= 1
                            self.direction = 180
                            if debug is True:
                                print("\n\nMOVED SUCCESSFULLY!!!!\n\n")
                        elif my_cell_number + 1 == cell_number:
                            self.rect.y += 100
                            self.node_y += 1
                            self.direction = 270
                            if debug is True:
                                print("\n\nMOVED SUCCESSFULLY!!!!\n\n")
                        elif my_cell_number - 1 == cell_number:
                            self.rect.y -= 100
                            self.node_y -= 1
                            self.direction = 90
                            if debug is True:
                                print("\n\nMOVED SUCCESSFULLY!!!!\n\n")
                        else:
                            pygame.quit()
                    except:
                        pass
                
    def update(self, cells, player_node_y, player_node_x):
        if self.destroyed is False:
            #print("\nPlayer Node: " + str(player_node_y) + ", " + str(player_node_x))
            #print("TIMER: " + str(self.shoot_timer))
            if self.node_x >= player_node_y:
                player_range_x = self.node_x - player_node_y
            else:
                player_range_x = player_node_y - self.node_x
            if self.node_y >= player_node_x:
                player_range_y = self.node_y - player_node_x
            else:
                player_range_y = player_node_x - self.node_y
            #print("Player Range x: " + str(player_range_x) + " | Player Range y: " + str(player_range_y))
            if player_range_x <= 2 and self.node_y == player_node_x:
                #print("Player in range A!")
                #print("Player Node X: " + str(player_node_y) + "\nMy Node X: " + str(self.node_x))
                if player_node_y > self.node_x:
                    self.direction = 0
                    self.shoot = True
                else:
                    self.direction = 180
                    self.shoot = True
            elif player_range_y <= 2 and self.node_x == player_node_y:
                #print("Player in range B!")
                #print("Player Node X: " + str(player_node_x) + "\nMy Node X: " + str(self.node_y))
                if player_node_x > self.node_y:
                    self.direction = 270
                    self.shoot = True
                else:
                    self.direction = 90
                    self.shoot = True
            else:
                self.shoot = False
                self.path_find_timer -= 1
                if self.path_find_timer < 1:
                    self.path = path_find(cells, self.node_x, self.node_y, player_node_x, player_node_y)
                    if self.path != None:
                        self.path.pop(0)
                    self.path_find_timer = 1000
                self.enemy_move(False)
            if self.shoot is True:
                self.shoot_timer -= 1
            if self.shoot is True and self.shoot_timer < 1:
                self.shoot_timer = 50
                if self.direction == 0:
                    return [True, self.rect.x + 62, self.rect.y + 30, self.node_x, self.node_y, self.direction]
                if self.direction == 90:
                    return [True, self.rect.x + 30, self.rect.y + 1, self.node_x, self.node_y, self.direction]
                if self.direction == 180:
                    return [True, self.rect.x + 1, self.rect.y + 28, self.node_x, self.node_y, self.direction]
                if self.direction == 270:
                    return [True, self.rect.x + 28, self.rect.y + 62, self.node_x, self.node_y, self.direction]
            else:
                return [False, None, None, None, None, None]
        else:
            return [False, None, None, None, None, None]

    def draw(self, target):
        if self.destroyed is False:
            if self.direction == 0:
                target.blit(self.image_right, (self.rect.x - 32, self.rect.y - 32))
            if self.direction == 90:
                target.blit(self.image_up, (self.rect.x - 32, self.rect.y - 32))
            if self.direction == 180:
                target.blit(self.image_left, (self.rect.x - 32, self.rect.y - 32))
            if self.direction == 270:
                target.blit(self.image_down, (self.rect.x - 32, self.rect.y - 32))
            #pygame.draw.circle(target, (0, 255, 0), (self.rect.x, self.rect.y), 8)
            return False
        else:
            target.blit(self.image_destroyed, (self.rect.x - 32, self.rect.y - 32))
            self.despawn_timer -= 1
            if self.despawn_timer < 1:
                return True
            else:
                return False

class EnemyBullet(Sprite):
    def __init__(self, x, y, node_x, node_y, direction):
        super().__init__()
        self.node_x = node_x
        self.node_y = node_y
        self.image = pygame.image.load("Sprites\\Player\\spr_player_bullet.png").convert()
        self.image = pygame.transform.rotate(self.image, direction)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.node_increase = 0
        self.speed = 5

    def update(self, cells, screen_info):
        if self.direction == 0:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.x += self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_x += 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 90:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.y -= self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_y -= 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 180:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.x -= self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_x -= 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.direction == 270:
            if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                return True
            self.rect.y += self.speed
            self.node_increase += self.speed
            if self.node_increase >= 100:
                self.node_y += 1
                if check_next_node(self.direction, cells, self.node_x, self.node_y) is False:
                    return True
                else:
                    self.node_increase = 0
        if self.rect.x >= screen_info["width"] or self.rect.x <= 0:
            return True
        if self.rect.y >= screen_info["height"] or self.rect.y <= 0:
            return True
        return False

    def draw(self, target):
        target.blit(self.image, (self.rect.x - 32, self.rect.y - 32))

class DeadEnemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.image_destroyed = pygame.image.load("Sprites\\Enemy\\spr_enemy_destroyed.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.despawn_timer = 1000

    def update(self):
        self.despawn_timer -= 1
        if self.despawn_timer < 1:
            return True
        else:
            return False
    def draw(self, target):
        target.blit(self.image, (self.rect.x - 32, self.rect.y - 32))
