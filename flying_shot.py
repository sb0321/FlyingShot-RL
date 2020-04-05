import pygame
import random
from time import sleep

class GAME:

    def __init__(self):

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.pad_width = 480
        self.pad_height = 320
        self.background_width = 740
        self.aircraft_width = 90
        self.aircraft_height = 55

        self.background1_x = 0
        self.background2_x = self.background_width

        self.bat_width = 110
        self.bat_height = 67

        self.bat_x = self.pad_width
        self.bat_y = random.randrange(0, self.pad_height - self.bat_height)

        self.fire = None
        self.fire_x = self.pad_width
        self.fire_y = random.randrange(0, self.pad_height)



        self.fireball1_width = 140
        self.fireball1_height = 60
        self.fireball2_width = 86
        self.fireball2_height = 60

        self.isShotBat =False
        self.shot_bat_count = 0
        self.boom_count = 0

        self.bullet_xy = []

        self.action_space = 3

        self.x = self.pad_width * 0.05
        self.y = self.pad_height / 2

        self.done = False

        pygame.init()
        pygame.display.set_caption("FlyingShot")
        self.gamepad = pygame.display.set_mode((self.pad_width, self.pad_height))


        # init game
        self.initGame()

    def restart(self):

        pygame.display.set_mode()

        del self.fires
        self. fires = []
        self.fires.append((0, self.fireball1_shape))
        self.fires.append((1, self.fireball2_shape))

        self.shot_bat_count = 0
        self.isShotBat = False

        for i in range(3):
            self.fires.append((i + 2, None))

        random.shuffle(self.fires)
        self.fire = self.fires[0]

        self.fire_x = -30
        self.fire_y = random.randrange(0, self.pad_height)

        self.bat_x = self.pad_width
        self.bat_y = random.randrange(0, self.pad_height - self.bat_height)

        self.bullet_xy.clear()

        self.x = self.pad_width * 0.05
        self.y = self.pad_height / 2
        self.done = False



    def initGame(self):
        #pygame.display.set_mode()

        self.state = pygame.surfarray.array3d(self.gamepad)

        self.aircraft = pygame.image.load('images/plane.png')

        self.background1 = pygame.image.load('images/background.png')
        self.background2 = self.background1.copy()

        self.bat = pygame.image.load('images/bat.png')

        self.fires = []
        self.fireball1_shape = pygame.image.load('images/fireball.png')
        self.fireball2_shape = pygame.image.load('images/fireball2.png')
        self.fires.append((0, self.fireball1_shape))
        self.fires.append((1, self.fireball2_shape))

        for i in range(3):
            self.fires.append((i + 2, None))

        random.shuffle(self.fires)
        self.fire = self.fires[0]

        self.fire_x = -30
        self.fire_y = random.randrange(0, self.pad_height)


        self.bat_x = self.pad_width
        self.bat_y = random.randrange(0, self.pad_height - self.bat_height)

        self.bullet = pygame.image.load('images/bullet.png')

        self.boom = pygame.image.load('images/boom.png')

        self.clock = pygame.time.Clock()

        self.done = False



    def textObj(self, text, font):
        texSurface = font.render(text, True, self.RED)
        return texSurface, texSurface.get_rect()

    def dispMessage(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.textObj(text, largeText)
        TextRect.center = ((self.pad_width / 2), (self.pad_height / 2))
        self.gamepad.blit(TextSurf, TextRect)
        pygame.display.update()

    def crash(self):
        self.dispMessage('Crashed!')
        sleep(3)

    def drawObject(self, obj, x, y):
        self.gamepad.blit(obj, (x, y))

    def back(self, background, x, y):
        self.gamepad.blit(background, (x, y))

    def control(self):

        action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # y_change = -5
                    action = pygame.K_UP
                elif event.key == pygame.K_DOWN:
                    # y_change = 5
                    action = pygame.K_DOWN
                elif event.key == pygame.K_a:
                    action = pygame.K_a
            #if event.type == pygame.KEYUP:
            #    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #        y_change = 0

        return action

    def movement(self, action):

        y_change = 0

        if action == pygame.K_UP:
            y_change = -10
        elif action == pygame.K_DOWN:
            y_change = 10
        else:
            y_change = 0

        return y_change

    def action_translate(self, raw_action):

        action = None

        if raw_action == 0:
            action = pygame.K_UP
        elif raw_action == 1:
            action = pygame.K_DOWN
        else:
            action = pygame.K_a

        return action

    def shoot_bullet(self, action):
        # 총을 한번 쏠때마다 리워드 감소
        isShot = False
        if action == pygame.K_a:
            bullet_x = self.x + self.aircraft_width
            bullet_y = self.y + self.aircraft_height / 2
            self.bullet_xy.append([bullet_x, bullet_y])
            isShot = True

        return isShot

    def render_fireball(self):
        # fireball
        if self.fire == None:
            self.fire_x -= 30
        else:
            self.fire_x -= 10

        if self.fire_x <= 0:
            self.fire_x = self.pad_width
            self.fire_y = random.randrange(0, self.pad_height)
            random.shuffle(self.fires)
            self.fire = self.fires[0]

        if self.fire[1] != None:
            self.drawObject(self.fire[1], self.fire_x, self.fire_y)

    def render_aircraft(self):
        # aircraft
        self.drawObject(self.aircraft, self.x, self.y)

    def render_background(self):
        # background
        self.background1_x -= 2
        self.background2_x -= 2
        if self.background1_x == -self.background_width:
            background1_x = self.background_width
        if self.background2_x == -self.background_width:
            background2_x = self.background_width

        self.drawObject(self.background1, self.background1_x, 0)
        self.drawObject(self.background2, self.background2_x, 0)


    def render_bat(self):
        # bat
        self.bat_x -= 7
        if self.bat_x <= 0:
            self.bat_x = self.pad_width
            self.bat_y = random.randrange(0, self.pad_height - self.bat_height)

        self.drawObject(self.bat, self.bat_x, self.bat_y)


    def render_bullet(self):

        # 총알이 박쥐에 맞았을 경우 보상

        # bullet
        if len(self.bullet_xy) != 0:
            for i, bxy in enumerate(self.bullet_xy):
                bxy[0] += 15
                self.bullet_xy[i][0] = bxy[0]

                # 총알이 박쥐에 맞았을 경우
                if bxy[0] > self.bat_x:
                    if bxy[1] > self.bat_y and bxy[1] < self.bat_y + self.bat_height:
                        # 총알 없애기
                        self.bullet_xy.remove(bxy)
                        self.isShotBat = True
                        self.shot_bat_count += 1

                if bxy[0] > self.pad_width:
                    try:
                        self.bullet_xy.remove(bxy)
                    except:
                        pass

        if not self.isShotBat:
            self.drawObject(self.bat, self.bat_x, self.bat_y)
        else:
            self.drawObject(self.boom, self.bat_x, self.bat_y)
            self.boom_count = 0
            self.bat_x = self.pad_width
            self.bat_y = random.randrange(0, self.pad_height - self.bat_height)
            self.isShotBat = False

        if len(self.bullet_xy) != 0:
            for bx, by in self.bullet_xy:
                self.drawObject(self.bullet, bx, by)



    def render_collide(self):
        
        # 박쥐나 불꽃에 부딫혔을 경우 보상
        done = False

        # check aircraft crashed by BAT
        if self.x + self.aircraft_width > self.bat_x:
            if (self.y > self.bat_y and self.y < self.bat_y + self.bat_height) or (
                    self.y + self.aircraft_height > self.bat_y and self.y + self.aircraft_height < self.bat_y + self.bat_height):
                print("박쥐 충돌")
                done = True

        # check fireball
        if self.fire[1] != None:
            if self.fire[0] == 0:
                fireball_width = self.fireball1_width
                fireball_height = self.fireball1_height
            elif self.fire[0] == 1:
                fireball_width = self.fireball2_width
                fireball_height = self.fireball2_height
            else:
                fireball_height = 0

            # 파이어볼에 맞을경우
            if self.x + self.aircraft_width > self.fire_x:
                if (self.y > self.fire_y and self.y < self.fire_y + fireball_height) or (
                        self.y + self.aircraft_height > self.fire_y and self.y + self.aircraft_height < self.fire_y + fireball_height):
                    print("불 충돌")
                    done = True
                else:
                    pass
        else:
            pass

        return done


    def update(self):
        pygame.display.update()
        #self.clock.tick(15)

    def game_init(self):
        state, _, _, _, _ = self.step(random.randint(0,2))
        return state



    def step(self, action):

        # 컴퓨터가 알아서 하므로
        pygame.event.pump()
        #컴퓨터가 할 때
        action = self.action_translate(action)
        y_change = self.movement(action)

        if self.done == True:
            self.restart()
            self.done = False

        if self.state is not None:
            del self.state

        #init
        # 스텝당 리워드
        reward = 0
        # 행동으로 y_값 변함
        # 사람이 할 때
        #action = self.control()
        #y_change = self.movement(action)



        # 총을 쏘는지 결정
        isShot = self.shoot_bullet(action)

        self.gamepad.fill(self.WHITE)
        
        # 환경 요소를 렌더링
        #self.render_background()
        self.render_aircraft()
        self.render_fireball()
        self.render_bullet()
        self.render_bat()
        hit = self.render_collide()


        # 범위 벗어나지 않게 움직이기
        if self.y <= 0:
            self.y += 10
        else:
            self.y += y_change


        if self.y >= self.pad_height - self.aircraft_height:
            self.y -= 10
        else:
            self.y += y_change

        self.update()
        
        # 현재 상태를 넘겨주기 위한 과정
        self.get_screen = pygame.surfarray.array3d(pygame.display.get_surface())
        self.state = self.get_screen

        win = None
        if self.shot_bat_count >= 10:
            self.done = True
            reward = 1
            win = True

        if hit == True:
            self.done = True
            reward = -1
            win = False

        #if isShot == True:
        #    reward = -0.1

        return self.state, reward, self.done, win, self.shot_bat_count


