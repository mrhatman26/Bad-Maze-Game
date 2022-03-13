import pygame
from pathing import load_cells, draw_maze, cells_converter
from objects import Player, PlayerBullet, Enemy, EnemyBullet, DeadEnemy
import random
import sys
import pprint
#Startup
pygame.init()
restart = True
#Main Loop
def main_loop():
    screen_info = {
        "width": 1000,
        "height": 1000,
    }
    screen_info["screen"] = pygame.display.set_mode((screen_info["width"], screen_info["height"]))
    game_run = True
    #Global Vars
    cells = load_cells()
    cells_converted = cells_converter(cells)
    enemy_spawn_timer = 0#3000
    max_enemies = 10
    max_enemies -= 1
    applicable_directions = [0, 90, 180, 270]
    score = 0
    player_health_text = pygame.font.SysFont("Helvetica", 20, True, False)
    player_score_text = pygame.font.SysFont("Helvetica", 80, True, False)
    game_over_text = pygame.font.SysFont("Helvetica", 160, True, False)
    game_over_control_text = pygame.font.SysFont("Helvetica", 40, True, False)
    save_score_control_text = pygame.font.SysFont("Helvetica", 40, True, False)
    #print(len(cells_converted))
    #pprint.pprint(cells_converted)
    #sys.exit()
    #Object Creation
    player_start_node_x = random.randint(1, 10)
    player_start_node_y = random.randint(1, 10)
    player_start_x = player_start_node_x * 100
    player_start_x -= 50
    player_start_y = player_start_node_y * 100
    player_start_y -= 50
    player = Player(player_start_x, player_start_y, player_start_node_x, player_start_node_y, applicable_directions[random.randint(0, 3)])#Player(50, 50, 1, 1, 0)
    enemies = pygame.sprite.Group()#Enemy(950, 950, 10, 10, 0)
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    dead_enemies = pygame.sprite.Group()
    game_run = True
    game_over = False
    saved_score = False
    while game_run is True:
        #Events:
        if player.health < 1:
            game_over = True
        if len(enemies) <= 5 and game_over is False:
            enemy_spawn_timer -= 1
        for event in pygame.event.get():
            #-Misc
            #-Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False
                    return False
                if event.key == pygame.K_r:
                    game_run = False
                    return True
                if game_over is False:
                    player.move_player(cells, event)
                    #print("X: " + str(player.rect.x) + "\nY: " + str(player.rect.y))
                    player_shoot_var = player.shoot_check(event)
                    if player_shoot_var != None:
                        player_bullets.add(PlayerBullet(player_shoot_var[0], player_shoot_var[1], player.node_x, player.node_y, player.direction))
                else:
                    if event.key == pygame.K_s:
                        if saved_score is False:
                            save_file = open("scores.txt", "a")
                            score_text = "\nScore: " + str(score)
                            save_file.write(score_text)
                            save_file.close()
                            saved_score = True
        #Object Updating:
        if game_over is False:
            player.update()
            for enemy in enemies:
                enemy_shoot = enemy.update(cells_converted, player.node_x, player.node_y)
                if enemy_shoot[0] is True:
                    enemy_bullets.add(EnemyBullet(enemy_shoot[1], enemy_shoot[2], enemy_shoot[3], enemy_shoot[4], enemy_shoot[5]))
                if pygame.sprite.groupcollide(player_bullets, enemies, True, True):#False):
                    score += 1
                    dead_enemies.add(DeadEnemy(enemy.rect.x, enemy.rect.y))
                    #enemies.remove(enemy)
            for bullet in player_bullets:
                if bullet.update(cells, screen_info) is True:
                    player_bullets.remove(bullet)
            for bullet in enemy_bullets:
                if bullet.update(cells, screen_info) is True:
                    enemy_bullets.remove(bullet)
            if enemy_spawn_timer < 1:
                if len(enemies) <= max_enemies:
                    enemy_node_x = random.randint(1, 10)
                    enemy_node_y = random.randint(1, 10)
                    enemy_x = enemy_node_x * 100
                    enemy_x -= 50
                    enemy_y = enemy_node_y * 100
                    enemy_y -= 50
                    enemies.add(Enemy(enemy_x, enemy_y, enemy_node_x, enemy_node_y, applicable_directions[random.randint(0, 3)]))#enemies.add(Enemy(enemy_x, enemy_y, enemy_node_x, enemy_node_y, direction[random.randint(0, 3)]))
                enemy_spawn_timer = 3000
            if pygame.sprite.spritecollide(player, enemy_bullets, True):
                player.health -= 10
            for dead in dead_enemies:
                despawn = dead.update()
                if despawn is True:
                    dead_enemies.remove(dead)
            player_health_surface = player_health_text.render(str(player.health), False, (255, 255, 255))
            player_score_surface = player_score_text.render(str(score), False, (255, 255, 255))
            screen_info["screen"].fill((0, 0, 0))
        else:
            screen_info["screen"].fill((0, 0, 0))
            player_score_surface = player_score_text.render("Final Score: " + str(score), False, (255, 255, 255))
            game_over_surface = game_over_text.render("GAME OVER", False, (255, 0, 0))
            game_over_control_surface = game_over_control_text.render("To try again, press R. To quit, press ESC.", False, (255, 255, 255))
            if saved_score is False:
                save_score_control_surface = save_score_control_text.render("To save your score, press S", False, (0, 255, 0))
            else:
                save_score_control_surface = save_score_control_text.render("SCORE SAVED!", False, (0, 255, 0))
        #Drawing:
        player.draw(screen_info["screen"], game_over)
        if game_over is False:
            for enemy in enemies:
                despawn = enemy.draw(screen_info["screen"])
                if despawn is True:
                    enemies.remove(enemy)
            for bullet in player_bullets:
                bullet.draw(screen_info["screen"])
            for bullet in enemy_bullets:
                bullet.draw(screen_info["screen"])
            for dead in dead_enemies:
                dead.draw(screen_info["screen"])
            draw_maze(screen_info, cells)
            screen_info["screen"].blit(player_health_surface, (player.rect.x - 16, player.rect.y - 10))
            screen_info["screen"].blit(player_score_surface, (475, 900))
        else:
            screen_info["screen"].blit(game_over_surface, (100, 250))
            screen_info["screen"].blit(player_score_surface, (300, 400))
            screen_info["screen"].blit(game_over_control_surface, (200, 500))
            if saved_score is False:
                screen_info["screen"].blit(save_score_control_surface, (300, 550))
            else:
                screen_info["screen"].blit(save_score_control_surface, (375, 550))
        pygame.display.update()
while restart is True: #If restart is true, this will restart the game (When R is pressed) else it will end the game (When Escape is pressed)
    restart = main_loop()
pygame.quit()
