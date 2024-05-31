import pygame

pygame.init()

WHITE = 255, 255, 255
GREEN = 50, 255, 125
BLUE = 0, 175, 255
BLACK = 0, 0, 0
RED = 255, 0, 0

WIDTH = 800
HEIGHT = 800

PLAYER_X = 50
PLAYER_Y = 650

TICK = 70


class Platform:
    colors = {
        1: BLACK,
        2: RED
    }
    
    def __init__(self, x, y, w, h, type):
        self.type = type
        self.x = x 
        self.y = y
        self.w = w
        self.h = h

    def render(self):
        rect = [self.x, self.y, self.w, self.h]
        color = Platform.colors[self.type]
        pygame.draw.rect(screen, color, rect)


class Player:
    color = BLUE
    max_vel = 20
    size = 30
    
    def __init__(self, x, y):
        self.friction = .9
        self.gravity = .3
        self.jump = 8
        self.walk = 4

        self.xvel = 0
        self.yvel = 0
        self.x = x
        self.y = y

    def render(self):
        rect = [self.x, self.y, Player.size, Player.size]
        pygame.draw.rect(screen, Player.color, rect)

    def touching_right(self):
        for platform in platforms:
            within_x = self.x + Player.size >= platform.x and \
                       self.x + Player.size < platform.x + self.walk
            within_y = self.y + Player.size > platform.y and \
                       self.y < platform.y + platform.h
            if within_x and within_y:
                self.x = platform.x - Player.size
                return platform.type
        return 0     

    def touching_left(self):
        for platform in platforms:
            within_x = self.x <= platform.x + platform.w and \
                       self.x + self.walk > platform.x + platform.w
            within_y = self.y + Player.size > platform.y and \
                       self.y < platform.y + platform.h
            if within_x and within_y:
                self.x = platform.x + platform.w
                return platform.type
        return 0

    def touching_ground(self):
        for platform in platforms:
            within_x = self.x + Player.size > platform.x and \
                       self.x < platform.x + platform.w
            within_y = self.y + Player.size > platform.y and \
                       self.y + Player.size < platform.y + Player.max_vel
            if within_x and within_y:
                self.y = platform.y - self.size
                return platform.type
        return 0

    def touching_ceiling(self):
        for platform in platforms:
            within_x = self.x + Player.size > platform.x and \
                       self.x < platform.x + platform.w
            within_y = self.y < platform.y + platform.h and \
                       self.y + self.jump > platform.y + platform.h
            if within_x and within_y:
                self.y = platform.y + platform.h
                return platform.type
        return 0

    def move(self, keys):
        right = self.touching_right()
        left = self.touching_left()
        ground = self.touching_ground()
        ceiling = self.touching_ceiling()

        if 2 in (left, right, ground, ceiling):
            self.__init__(PLAYER_X, PLAYER_Y)

        if pygame.K_LEFT in keys:
            self.xvel = -self.walk
        if pygame.K_RIGHT in keys:
            self.xvel = self.walk

        if pygame.K_UP in keys and ground:
            self.yvel = -self.jump

        if self.yvel < Player.max_vel:
            self.yvel += self.gravity

        if self.xvel > 0 and right:
            self.xvel = 0
        if self.xvel < 0 and left:
            self.xvel = 0
        if self.yvel > 0 and ground:
            self.yvel = 0
        if self.yvel < 0 and ceiling:
            self.yvel = 0

        self.xvel *= self.friction

        self.x += self.xvel
        self.y += self.yvel


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Platformer Engine')

clock = pygame.time.Clock()

player = Player(PLAYER_X, PLAYER_Y)
platforms = []

drawing = True

drag = False
rectx = None
recty = None
rectt = 1

keys = []
done = False
while not done:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN and drawing:
            rectx, recty = mx, my
            drag = True

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            rectw, recth = abs(mx - rectx), abs(my - recty)
            platforms.append(Platform(rectx, recty, rectw, recth, rectt))
            drag = False

        if event.type == pygame.KEYDOWN:
            keys.append(event.key)
            
            if event.key == pygame.K_c:
                platforms = []

            if event.key == pygame.K_1:
                rectt = 1

            if event.key == pygame.K_2:
                rectt = 2

            if event.key == pygame.K_SPACE:
                drawing = not drawing
                player.__init__(PLAYER_X, PLAYER_Y)

        if event.type == pygame.KEYUP:
            try:
                keys.remove(event.key)
            except ValueError:
                pass

    if not drawing:
        player.move(keys)

    screen.fill(WHITE)

    if drag:
        rectw, recth = abs(mx - rectx), abs(my - recty)
        pygame.draw.rect(screen, Platform.colors[rectt],
                        [rectx, recty, rectw, recth])

    player.render()
    for platform in platforms:
        platform.render()
    
    pygame.display.update()
    clock.tick(TICK)

pygame.quit()
