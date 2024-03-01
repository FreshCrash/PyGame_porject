import csv
import sys
import time
import pygame
import json
gforce = 1
speed = 5

Ship_up = pygame.image.load("Data/Images/Ship_up.png")
Ship_down = pygame.image.load("Data/Images/Ship_down.png")
cube_img = pygame.image.load("Data/Images/Player.png")
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)
        self.image = cube_img
        self.rect = pygame.Rect((100, 0, 50, 50))
        self.gamemode = "Cube"
        self.speed = 0
        self.gforce = 1
        self.flip = 1
    def update(self):
        if pygame.sprite.spritecollideany(self, kill_objects):
            self.rect.y -= self.speed
            if pygame.sprite.spritecollideany(self, kill_objects):
                self.explode()
            self.rect.y += self.speed
        if pygame.sprite.spritecollideany(self, inst_k):
            self.explode()
        if pygame.sprite.spritecollideany(self, objects):
            self.speed = 0

            while pygame.sprite.spritecollideany(self, objects):
                self.rect.y -= 1 * self.gforce
            if self.gamemode == "Cube":
                self.rect.y += 1
        else:
            self.speed += self.gforce * self.flip
            self.rect.y += self.speed
    def jump(self):
        if self.gamemode == "Cube":
            if pygame.sprite.spritecollideany(self, objects):
                while pygame.sprite.spritecollideany(self, objects):
                    self.rect.y -= self.gforce
                self.speed = -17 * self.gforce
        elif self.gamemode == "Ship":
            self.flip = -1
            player.image = Ship_up
    def released(self):
        if self.gamemode == "Ship":
            self.flip = 1
            player.image = Ship_down
    def explode(self):
        global Alive
        Alive = False
        clear_all()

class spike(pygame.sprite.Sprite):
    def __init__(self, x, y, color, flip, *groups):
        super().__init__(groups)
        self.image = pygame.image.load("Data/Images/Spike.png")
        if flip == 1:
            self.image = pygame.transform.flip(self.image, 0, 1)
        self.rect = pygame.Rect((x, y, 50, 50))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.x -= speed
        if pygame.sprite.collide_mask(self, player):
            player.explode()

def clear_all():
    for object in all_sprites:
        if object is not player and object not in floor_group:
            object.kill()

class gamemode_portal(pygame.sprite.Sprite):
    def __init__(self, x, y, mode , *groups):
        self.mode = mode
        super().__init__(groups)
        self.image = pygame.Surface((50, 50),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 0, 255), (0, 0, 50, 50))
        self.rect = pygame.Rect((x, y, 50, 50))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.x -= speed
        if pygame.sprite.collide_mask(self, player):
            player.gamemode = self.mode
            if self.mode == "Ship":
                player.image = Ship_down
            elif self.mode == "Cube":
                player.image = cube_img
                player.flip = 1





class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups, color=(0, 0, 255)):
        super().__init__(groups)
        self.image = pygame.Surface((800, 50),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color, (0, 0, 800, 50))
        self.rect = pygame.Rect((0, 350, 800, 50))


class standard_block(pygame.sprite.Sprite):
    def __init__(self, color, y_pos, *groups):
        super().__init__(groups)
        kill_block((100, 100, 100, 50), y_pos + 5, all_sprites, kill_objects)
        self.image = pygame.image.load("Data/Images/Block.png")
        self.rect = pygame.Rect((800, y_pos, 50, 50))
    def update(self):
        self.rect.x -= speed

class kill_block(pygame.sprite.Sprite):
    def __init__(self, color, y_pos, *groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 40),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color, (0, 0, 50, 40))
        self.rect = pygame.Rect((800, y_pos, 50, 40))
    def update(self):
        self.rect.x -= speed

def menu(bg_color):
    global levels
    currlvl = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_RIGHT:
                    currlvl += 1
                    currlvl %= len(levels)
                if event.key == pygame.K_LEFT:
                    currlvl -= 1
                    currlvl %= len(levels)
                if event.key == pygame.K_SPACE:
                    while True:
                        r = load_level(levels[currlvl])
                        print(r)
                        if r == 0:
                            break

        screen.fill(bg_color)
        font = pygame.font.Font(None, 50)
        text = font.render(levels[currlvl], True, (100, 255, 100))
        screen.blit(text, (200, 200))
        clock.tick(60)
        pygame.display.flip()

def load_level(levelname):
    global Alive
    global bgcolor
    tomenu = False
    levelcsv = csv.reader(open("Levels/" + levelname + "/Level.csv"), delimiter=",")
    dat = json.load(open("Levels/" + levelname + "/data.json"))
    clr = dat["bgcolor"]
    bgcolor = tuple(clr)
    pygame.mixer.music.load("Levels/" + levelname + "/Music.mp3")
    pygame.mixer.music.play(1)
    player.rect.y = 300
    player.image = cube_img
    player.speed = 0
    player.flip = 1
    level = []
    for row in levelcsv:
        level.append(row)
    load_row = pygame.USEREVENT + 1
    col = 0
    pygame.time.set_timer(load_row, 800 // speed)
    Alive = True
    while Alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    standard_block((255, 0, 0), 300, all_sprites, objects)
                elif event.key == pygame.K_s:
                    player.gamemode = "Ship"
                elif event.key == pygame.K_c:
                    player.gamemode = "Cube"
                elif event.key == pygame.K_q:
                    spike(800, 300, (255, 255, 255), 0, all_sprites)
                elif event.key == pygame.K_ESCAPE:
                    tomenu = True
                    pygame.mixer.music.stop()
                    Alive = False
            elif event.type == load_row:
                level_len = len(level[0])
                level_h = len(level)
                if col < level_len:
                    for ind, row in enumerate(level):
                        if col < len(row):
                            if row[col] == "Block":
                                standard_block((255, 0, 0), ind * 50, all_sprites, objects)
                            elif row[col] == "Spike":
                                spike(800, ind * 50, (255, 255, 255), 0, all_sprites, kill_objects)
                            elif row[col] == "Spike_f":
                                spike(800, ind * 50, (255, 255, 255), 1, all_sprites, kill_objects)
                            elif row[col][:3:] == "gm_":
                                gamemode_portal(800, ind * 50, row[col][3::], all_sprites)
                            elif row[col] == "end":
                                return lv_end()
                col += 1
        all_sprites.update()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or mouse[0]:
            player.jump()
        else:
            player.released()
        clock.tick(60)


        screen.fill(bgcolor)
        all_sprites.draw(screen)
        pygame.display.flip()

    clear_all()
    player.gamemode = "Cube"
    if not tomenu:
        return levelname
    else:
        return 0


def lv_end():
    pygame.mixer.music.stop()
    clear_all()
    font = pygame.font.Font(None, 50)
    text = font.render("Level complete!", True, (100, 255, 100))
    screen.blit(text, (200, 200))
    pygame.display.flip()
    time.sleep(1)
    return 0


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('GD')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    levels = ["Tutorial Cube", "Tutorial Ship", "Ultimate destruction"]
    all_sprites = pygame.sprite.Group()
    objects = pygame.sprite.Group()
    kill_objects = pygame.sprite.Group()
    inst_k = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    player = Player(all_sprites)
    Alive = True
    floor = Floor(all_sprites, objects, floor_group)
    clock = pygame.time.Clock()
    menu((0, 0, 0))
