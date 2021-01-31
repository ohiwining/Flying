import pygame
from random import randint as Rint

# Settings
Screen_Width, Screen_Height = 480, 640
HitPoint = -20
iScore, iFireMode, iFireFreq, iSpeed = 0, 1,1,1
Enemy_Spawn_Time = 15
Cloud_Spawn_Time = 80
Supplies_Spawn_Time = 500
# Game Config
FPS = 60
Player_Width, Player_Height = 40, 40
Enemy_Width, Enemy_Height = 30, 30
Bullet_Width, Bullet_Height = 5, 10
Cloud_Width, Cloud_Height = 100, 100
Supply_Width, Supply_Height = 40, 40
# Color Constants
Black = (0, 0, 0)
White = (255, 255, 255)
Sky_Blue = (6, 209, 225)
Cloud_Color = (138, 248, 253)
Player_Color = (6, 13, 253)
Bullet_Color = (254, 12, 5)
# System Constants
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Flyer Gen2")
pygame.mouse.set_visible(True)


class Item(pygame.sprite.Sprite):
    def __init__(self, Width, Height, color, spawnX, spawnY):
        pygame.sprite.Sprite.__init__(self)  # Initial for super class
        self.image = pygame.Surface((Width, Height))  # Initial width and height
        self.image.fill(color)  # Color definition
        self.rect = self.image.get_rect()
        self.rect.x = spawnX  # Spawn position in x axis
        self.rect.y = spawnY  # Spawn position in y axis

    def update(self):
        # Define update actions for each sprite
        pass


class Bullet(Item):
    def __init__(self, spawnX, spawnY, x, y):
        super().__init__(Bullet_Width, Bullet_Height, Bullet_Color, spawnX, spawnY)
        # Bullet flying directions
        self.directX = x
        self.directY = y

    def update(self):
        # Update bullet position
        self.rect.x += self.directX
        self.rect.y += 10 * self.directY
        if self.rect.y < -Bullet_Height:
            self.kill()
            # Kill this spirit when it is not in the screen.


class Player(Item):
    def __init__(self, spawnX, spawnY):
        super().__init__(Player_Width, Player_Height, Player_Color, spawnX, spawnY)
        self.hp = 100
        self.lives = 3
        self.x_speed = iSpeed * Screen_Width / 180
        self.y_speed = iSpeed * Screen_Height / 180
        self.fireMode = iFireMode  # Different fire mode will cause various firing pattern.
        self.fireFreq = iFireFreq

    def update(self):
        key_state = pygame.key.get_pressed()
        # K_UP/DOWN/LEFT/RIGHT is corresponded with four arrow keys on the keyboard.
        if key_state[pygame.K_UP]:
            self.rect.y -= self.y_speed
        if key_state[pygame.K_DOWN]:
            self.rect.y += self.y_speed
        if key_state[pygame.K_LEFT]:
            self.rect.x -= self.x_speed
        if key_state[pygame.K_RIGHT]:
            self.rect.x += self.x_speed

        # Set player's position in screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > Screen_Width - Player_Width:
            self.rect.x = Screen_Width - Player_Width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > Screen_Height - Player_Height:
            self.rect.y = Screen_Height - Player_Height

        # Set player's attribute
        if self.lives > 3:
            self.lives = 3
        if self.hp > 100:
            self.hp = 100

    def fire(self, last_time, bullets):
        # This function can modify firing speed and fire pattern.
        now = pygame.time.get_ticks()
        if now - last_time > 200 / self.fireFreq:
            last_time = now
            if self.fireMode == 1:
                # One bullet at once, from middle.
                bullets.add(Bullet(self.rect.centerx, self.rect.y, 0, -1))
            elif self.fireMode == 2:
                # Two bullets at once, from left and right.
                bullets.add(Bullet(self.rect.x, self.rect.y, 0, -1))
                bullets.add(Bullet(self.rect.right - Bullet_Width, self.rect.y, 0, -1))
            elif self.fireMode == 3:
                # Three bullets at once, from left middle and right.
                bullets.add(Bullet(self.rect.x, self.rect.y, -1, -1))
                bullets.add(Bullet(self.rect.centerx - Bullet_Width / 2, self.rect.y, 0, -1))
                bullets.add(Bullet(self.rect.right - Bullet_Width, self.rect.y, 1, -1))
            elif self.fireMode > 3:
                # Five bullets at once, from left middle and right.
                bullets.add(Bullet(self.rect.centerx - Bullet_Width / 2, self.rect.y, 0, -1))
                bullets.add(Bullet(self.rect.x, self.rect.y, -1, -1))
                bullets.add(Bullet(self.rect.right - Bullet_Width, self.rect.y, 1, -1))
                bullets.add(Bullet(self.rect.x - Bullet_Width, self.rect.centery, -2, -1))
                bullets.add(Bullet(self.rect.right, self.rect.centery, 2, -1))
        return last_time

    def catch_supply(self, supplyType):
        global iSpeed
        if supplyType == 0:
            # Recover player's hp
            self.hp = 100
        elif supplyType == 1:
            # Add one more life to player.
            self.lives += 1
        elif supplyType == 2:
            # Change player's fire mode.
            self.fireMode += 1
        elif supplyType == 3:
            # Make player move faster
            iSpeed += 1
            self.x_speed = iSpeed * Screen_Width / 180
            self.y_speed = iSpeed * Screen_Height / 180
        elif supplyType == 4:
            self.fireFreq += 1

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Enemy(Item):
    def __init__(self, color, spawnX):
        super().__init__(Enemy_Width, Enemy_Width, color, spawnX, 0)
        # Enemy has 3 different dropping velocities. 1 pixel (per frame) minimal, 3 pixels max.
        self.velocity = Rint(1, 3)

    def update(self):
        self.rect.y += self.velocity + 1
        if self.rect.y > Screen_Height:
            self.kill()


class Cloud(Item):
    def __init__(self, spawnX):
        super().__init__(Cloud_Width, Cloud_Width, Cloud_Color, spawnX, 0)

    def update(self):
        self.rect.y += 1
        if self.rect.y > Screen_Height:
            self.kill()


class Supply(Item):
    def __init__(self, spawnX):
        # Supply color is set to black now, may change in the future.
        color = (0, 0, 0)
        super().__init__(Supply_Width, Supply_Height, color, spawnX, 0)

    def update(self):
        self.rect.y += 1
        if self.rect.y > Screen_Height:
            self.kill()


def show_text(text, size, centerX, centerY, color, font='Times New Roman'):
    # Display one sentence.
    font = pygame.font.Font(pygame.font.match_font(font), size)  # Set font and size.
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx, text_rect.centery = centerX, centerY  # Set position.
    screen.blit(text_surface, text_rect)


def show_HUD(score, player):
    # Display player's score, hp and the number of lives.
    show_text("Score: {}".format(score), 20, Screen_Width - 70, 35, White)
    pygame.draw.rect(screen, (0, 255, 0), (10, 15, player.hp, 15))  # Display HP
    pygame.draw.rect(screen, (255, 255, 255), (10, 15, 100, 15), 2)  # Edge of HP strip.
    for i in range(0, player.lives):
        pygame.draw.rect(screen, Player_Color, (30 * i + 15, 40, 20, 20))


def game_over(score):
    # Display final score and instructions.
    while True:
        screen.fill(Sky_Blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC key
                    exit(0)
                if event.key == pygame.K_RETURN:
                    return 1  # Return Player.lives

        show_text('You Lose!', 40, Screen_Width / 2, Screen_Height / 3, White)
        show_text("Your score:{}".format(score), 40, Screen_Width / 2, Screen_Height / 2, White)
        show_text("Press ESC to quit, Press ENTER to continue.", 25, Screen_Width / 2, Screen_Height * 2 / 3, White)
        pygame.display.flip()


def main():
    pygame.init()
    FramePerSec = pygame.time.Clock()
    player = Player(Screen_Width / 2, Screen_Height - Player_Height)
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    supplies = pygame.sprite.Group()
    score = iScore
    shoot = 0
    last_time = 0
    supplyType = 0
    while True:
        # Draw and update sprites
        FramePerSec.tick(FPS)
        screen.fill(Sky_Blue)
        clouds.draw(screen)
        supplies.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        screen.blit(player.image, player.rect)
        show_HUD(score, player)
        enemies.update()
        clouds.update()
        player.update()
        bullets.update()
        supplies.update()

        # System control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = 1 - shoot
                if event.key == pygame.K_ESCAPE:
                    exit(0)

        # Spawn sprites
        SupplyNum = str(supplies)[7:8]
        spawn_ticker = Rint(1, 1001)
        if spawn_ticker % Enemy_Spawn_Time == 0:
            enemy = Enemy((Rint(0, 255), Rint(0, 255), Rint(0, 255)), Rint(0, Screen_Width - Enemy_Width))
            enemies.add(enemy)
        if spawn_ticker % Cloud_Spawn_Time == 0:
            cloud = Cloud(Rint(-Cloud_Width, Screen_Width))
            clouds.add(cloud)
        if spawn_ticker % Supplies_Spawn_Time == 0 and SupplyNum == '0':
            supplyType = Rint(0, 4)
            supply = Supply(Rint(0, Screen_Width - Supply_Width))
            supplies.add(supply)
        if shoot == 1:
            last_time = player.fire(last_time, bullets)

        # If collide
        if pygame.sprite.spritecollide(player, enemies, True):
            player.hp += HitPoint
            if player.hp < 5:
                player.lives -= 1
                player.fireMode -= 1 if player.fireMode > 1 else 0
                player.hp = 100
                if player.lives == 0:
                    player.lives = game_over(score)
                    clouds.empty()
                    supplies.empty()
                    enemies.empty()
                    player.set_position(Screen_Width / 2, Screen_Height - Player_Height)
        if pygame.sprite.spritecollide(player, supplies, True):
            player.catch_supply(supplyType)
        if pygame.sprite.groupcollide(bullets, enemies, True, True):
            score += 1
        pygame.display.flip()


if __name__ == '__main__':
    main()
