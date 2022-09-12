from timeit import default_timer as timer

import math
import pygame
import random
from pygame import mixer

# init
pygame.init()
screen_width = 800
screen = pygame.display.set_mode((screen_width, 600))
pygame.display.set_caption("Inviders from space")
icon = pygame.image.load('img/menu/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 30

white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
global score_value


class Player:
    def __init__(self, player_id, player_x, player_y, player_x_change):
        self.playerImg = pygame.image.load(f'img/player/{player_id}.png')
        self.player_id = player_id
        self.player_x = player_x
        self.player_y = player_y
        self.player_x_change = player_x_change

    def mod_player_place(self, player_x, player_y, player_x_change):
        self.player_x = player_x
        self.player_y = player_y
        self.player_x_change = player_x_change

    def get_player_place(self):
        ls = [self.player_x, self.player_y, self.player_x_change]
        return ls

    def playerblit(self):
        global screen
        screen.blit(self.playerImg, (self.player_x, self.player_y))


class Bulet:
    def __init__(self, bulet_name, bulet_x, bulet_y, bulet_x_change, bulet_y_change, bullet_state):
        self.buletImg = pygame.image.load('img/player/action/bullet.png')
        self.bulet_name = bulet_name
        self.bulet_x = bulet_x
        self.bulet_y = bulet_y
        self.bulet_x_change = bulet_x_change
        self.bulet_y_change = bulet_y_change
        self.bullet_state = bullet_state

    def fire_bullet(self):
        self.bullet_state = "fire"
        global screen
        screen.blit(self.buletImg, (self.bulet_x + 16, self.bulet_y + 10))

    def get_bulet_place(self):
        ls = [self.bulet_x, self.bulet_y, self.bulet_x_change, self.bulet_y_change, self.bullet_state]
        return ls


class Enemy:
    def __init__(self, enemyid, enemy_lvl, enemy_x, enemy_y, enemy_x_change, enemy_y_change):
        self.enemyImg = pygame.image.load(f'img/enemy/{enemy_lvl}.png')
        self.enemyid = enemyid
        self.enemy_lvl = enemy_lvl
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.enemy_x_change = enemy_x_change
        self.enemy_y_change = enemy_y_change

    def get_place(self):
        ls = [self.enemyid, self.enemy_x, self.enemy_y, self.enemy_x_change, self.enemy_y_change]
        return ls

    def enemyblit(self):
        global screen
        screen.blit(self.enemyImg, (self.enemy_x, self.enemy_y))


class Level:
    def __init__(self, level_id, speed, enemy_num, level_time):
        self.levelImg = pygame.image.load(f'img/level/{level_id}.png').convert_alpha()
        self.level_id = level_id
        self.speed = speed
        self.enemy_num = enemy_num
        self.level_time = level_time
        self.levelStatus = "Lose"
        self.players = []
        self.enemies = []
        self.bulets = []

    def create_enemeis(self):
        for i in range(0, self.enemy_num - 1):
            new_enemy = Enemy(i, self.level_id, random.randint(0, 736), random.randint(50, 150), 4, 40)
            self.enemies.append(new_enemy)

    def create_player(self):
        new_player = Player("1", 370, 480, 0)
        self.players.append(new_player)

    def create_bulet(self):
        new_bulet = Bulet("1", 0, 480, 0, 10, "ready")
        self.bulets.append(new_bulet)

    @staticmethod
    def is_collision(enemy_x, enemy_y, bulet_x, bulet_y):
        distance = math.sqrt(math.pow(enemy_x - bulet_x, 2) + (math.pow(enemy_y - bulet_y, 2)))
        if distance < 27:
            return True
        else:
            return False

    @staticmethod
    def show_score(score_value):
        global screen
        font = pygame.font.Font('font/Begok.ttf', 30)
        score = font.render("score " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (10, 10))

    def show_level(self):
        global screen
        font = pygame.font.Font('font/Begok.ttf', 30)
        lvlnfo = font.render("level " + str(self.level_id), True, (255, 255, 255))
        screen.blit(lvlnfo, (330, 30))

    def chek_status(self, begin):
        global running
        now = timer()
        time_of_level = now - begin
        if self.level_time <= time_of_level:
            self.levelStatus = "Win"
            running = False
        else:
            pass

    def return_status(self):
        return self.levelStatus

    def run(self):
        begin = timer()
        global screen
        self.create_enemeis()
        self.create_player()
        self.create_bulet()

        global score_value
        global running
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(self.levelImg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.players[0].player_x_change = -4
                    if event.key == pygame.K_RIGHT:
                        self.players[0].player_x_change = 4
                    if event.key == pygame.K_SPACE:
                        if self.bulets[0].bullet_state == "ready":
                            shoot_sound = mixer.Sound("music/laser.wav")
                            shoot_sound.play()
                            self.bulets[0].bulet_x = self.players[0].player_x
                            self.bulets[0].fire_bullet()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.players[0].player_x_change = 0

            self.players[0].player_x += self.players[0].player_x_change
            if self.players[0].player_x <= 0:
                self.players[0].player_x = 0
            elif self.players[0].player_x >= 736:
                self.players[0].player_x = 736

            for i in range(0, self.enemy_num - 1):

                if self.enemies[i].enemy_y > 440:
                    for j in range(0, self.enemy_num - 1):
                        self.enemies[j].enemy_y = 2000
                    running = False
                    break

                self.enemies[i].enemy_x += self.enemies[i].enemy_x_change
                if self.enemies[i].enemy_x <= 0:
                    self.enemies[i].enemy_x_change = self.speed
                    self.enemies[i].enemy_y += self.enemies[i].enemy_y_change
                elif self.enemies[i].enemy_x >= 746:
                    self.enemies[i].enemy_x_change = -self.speed
                    self.enemies[i].enemy_y += self.enemies[i].enemy_y_change

                collision = self.is_collision(self.enemies[i].enemy_x, self.enemies[i].enemy_y, self.bulets[0].bulet_x,
                                              self.bulets[0].bulet_y)
                if collision:
                    explosion_sound = mixer.Sound("music/explosion.wav")
                    explosion_sound.play()
                    self.bulets[0].bulet_y = 480
                    self.bulets[0].bullet_state = "ready"
                    score_value += 1
                    self.enemies[i].enemy_x = random.randint(0, 746)
                    self.enemies[i].enemy_y = random.randint(50, 150)

                self.enemies[i].enemyblit()

            if self.bulets[0].bulet_y <= 0:
                self.bulets[0].bulet_y = 480
                self.bulets[0].bullet_state = "ready"

            if self.bulets[0].bullet_state == "fire":
                self.bulets[0].fire_bullet()
                self.bulets[0].bulet_y -= self.bulets[0].bulet_y_change

            self.players[0].playerblit()
            self.show_score(score_value)
            self.show_level()
            pygame.display.update()
            self.chek_status(begin)


def get_level_data(curent_level):
    w = ""
    with open('data/level.csv', "r") as fp:
        for m, line in enumerate(fp):
            if m == curent_level:
                w = line

    return w


def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, True, text_color)
    return new_text


def mid_scene(Status):
    menu_sound = mixer.Sound("music/music.wav")
    menu_sound.play(-1)
    tmp = True

    while tmp:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tmp = False
                menu_sound.stop()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_sound.stop()
                    tmp = False

        if tmp is True:
            background = pygame.image.load('img/menu/background.png')
            screen.blit(background, (0, 0))
            title = text_format("Inviders from space", 'font/Retro.ttf', 60, yellow)
            text_go = text_format("pres enter to continue", 'font/Begok.ttf', 20, gray)
            if Status == "win":
                text_sts = text_format("winner", 'font/Begok.ttf', 50, white)
            elif Status == "lvl":
                text_sts = text_format("level complited", 'font/Begok.ttf', 50, white)
            else:
                text_sts = text_format("you lose", 'font/Begok.ttf', 50, white)

            title_rect = title.get_rect()
            start_rect = text_sts.get_rect()
            quit_rect = text_go.get_rect()

            screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
            screen.blit(text_sts, (screen_width / 2 - (start_rect[2] / 2), 300))
            screen.blit(text_go, (screen_width / 2 - (quit_rect[2] / 2), 360))
            pygame.display.update()


def main_menu():
    menu_sound_is_play = False
    menu_sound = mixer.Sound("music/music.wav")
    global score_value
    score_value = 0
    global screen
    font = "font/Retro.ttf"
    menu = True
    selected = "start"

    while menu:
        if menu_sound_is_play is False:
            menu_sound.play(-1)
            menu_sound_is_play = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu_sound.stop()
                        menu_sound_is_play = False
                        run_game()
                    if selected == "quit":
                        pygame.quit()
                        quit()

        screen.fill(blue)
        background = pygame.image.load('img/menu/background.png')
        screen.blit(background, (0, 0))
        title = text_format("Inviders from space", font, 90, yellow)
        if selected == "start":
            text_start = text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, gray)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, gray)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(FPS)


def run_game():
    global screen
    curentLevel = 0
    play = True
    while play:
        lne = get_level_data(curentLevel)
        x = lne.split(';')
        lneId = int(x[0])
        lnespeed = int(x[0])
        lneenemy_num = int(x[2])
        lneenemy_tim = int(x[3])
        lvl = Level(lneId, lnespeed, lneenemy_num, lneenemy_tim)
        mixer.music.load("music/lvl.mp3")
        mixer.music.play(-1)
        lvl.run()
        mixer.music.stop()
        sts = lvl.return_status()
        if sts == "Win":
            if curentLevel == 4:
                play = False
                mid_scene("win")
            else:
                curentLevel += 1
                mid_scene("lvl")
        else:
            mid_scene("ovr")
            play = False

        pygame.display.update()
        clock.tick(FPS)


def main():
    main_menu()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
