import pygame
import random

WIDTH=480
HEIGHT=640
Sky_Blue=(6,209,225)
Enemy_RandColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
Cloud_Color=(138,248,253)
Player_Color=(6,13,253)
Bullet_Color=(254,12,5)
BLACK=(0,0,0)

class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((100,100))
		self.image.fill(Cloud_Color)
		self.rect=self.image.get_rect()
		self.rect.x=random.randint(-100,WIDTH)
	def update(self):
		self.rect.y+=1	

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((40,40))
		self.image.fill(Player_Color)
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.y=HEIGHT-40
		self.hp=100
		self.lives=3
	def update(self):
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_UP]:
			self.rect.y-=3
		if keystate[pygame.K_DOWN]:
			self.rect.y+=3
		if keystate[pygame.K_LEFT]:
			self.rect.x-=3
		if keystate[pygame.K_RIGHT]:
			self.rect.x+=3
		if self.rect.x<0:
			self.rect.x=0
		if self.rect.x>WIDTH-40:
			self.rect.x=WIDTH-40
		if self.rect.y>HEIGHT-40:
			self.rect.y=HEIGHT-40

class Enemy(pygame.sprite.Sprite):
	def __init__(self,newcolor):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((30,30))
		self.image.fill(newcolor)
		self.rect=self.image.get_rect()
		self.Velocity=random.randint(1,3)
		self.rect.x=random.randint(0,WIDTH-30)
	def update(self):
		if self.Velocity==1:
			self.rect.y+=2
		if self.Velocity==2:
			self.rect.y+=3
		if self.Velocity==3:
			self.rect.y+=4

class Bullet(pygame.sprite.Sprite):
	def __init__(self,positionx,positiony):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((5,10))
		self.image.fill(Bullet_Color)
		self.rect=self.image.get_rect()
		self.rect.x=positionx
		self.rect.y=positiony-30
	def update(self):
		self.rect.y-=10
		if self.rect.y<-50:
			self.kill()

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flyer")
pygame.mouse.set_visible(0)
FPS=pygame.time.Clock()
player=Player()
clouds=pygame.sprite.Group()
enemys=pygame.sprite.Group()
bullets=pygame.sprite.Group()
score=0
game_run=True
lasttime=0
fire=-1

def showscore():
	txt="Score: {}".format(score)
	font_name=pygame.font.match_font('Times New Roman')
	font=pygame.font.Font(font_name,20)
	text_surface=font.render(txt,True,(255,255,255))
	text_rect=text_surface.get_rect()
	text_rect.x=WIDTH-100
	text_rect.y=15
	screen.blit(text_surface,text_rect)
def draw_ui():
	pygame.draw.rect(screen,(0,255,0),(10,15,player.hp,15))
	pygame.draw.rect(screen,(255,255,255),(10,15,100,15),2)
	for i in range(0,player.lives):
		pygame.draw.rect(screen,Player_Color,(30*i+15,40,20,20))

while game_run:
	FPS.tick(60)
	positionx=player.rect.centerx
	positiony=player.rect.centery
	screen.fill(Sky_Blue)
	clouds.draw(screen)
	screen.blit(player.image,player.rect)
	enemys.draw(screen)
	bullets.draw(screen)
	showscore()
	draw_ui()
	enemys.update()
	clouds.update()
	player.update()
	bullets.update()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			exit(0)
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				fire=-fire
			if event.key==pygame.K_ESCAPE:
				exit(0)			
	Enemy_RandColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
	enemyspawn=random.randint(1,201)
	if enemyspawn%15==0:
		enemy=Enemy(Enemy_RandColor)
		enemys.add(enemy)
	cloudspawn=random.randint(1,201)
	if cloudspawn%80==0:
		cloud=Cloud()
		clouds.add(cloud)
	now=pygame.time.get_ticks()
	if fire==1:
		if now-lasttime>200:
			lasttime=now
			bullet=Bullet(positionx,positiony)
			bullets.add(bullet)
	collision=pygame.sprite.spritecollide(player,enemys,True)
	if collision:
		player.hp-=20
		if player.hp<5:
			player.lives-=1
			player.hp=100
			if player.lives<0:
				game_run=False
	if pygame.sprite.groupcollide(bullets,enemys,True,True):
		score+=1
	pygame.display.flip()

while 1:
	screen.fill(BLACK)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			exit(0)
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_ESCAPE:
				exit(0)
	txt="You lose!"
	font_name=pygame.font.match_font('Times New Roman')
	font=pygame.font.Font(font_name,40)
	text_surface=font.render(txt,True,(255,255,255))
	text_rect=text_surface.get_rect()
	text_rect.x=WIDTH/2-200
	text_rect.y=HEIGHT/2
	screen.blit(text_surface,text_rect)
	pygame.display.flip()
