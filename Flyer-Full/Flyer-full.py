import pygame
import random
from os import path

WIDTH=480
HEIGHT=640
Bullet_Color=(254,12,5)
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flyer")
data_dir=path.join(path.dirname(__file__),'Flyer_Full_data')
player_img=pygame.image.load(path.join(data_dir,'player.png')).convert()
back_img=pygame.image.load(path.join(data_dir,'back.png')).convert()
enemy_img=pygame.image.load(path.join(data_dir,'enemy.png')).convert()
cloud_img=pygame.image.load(path.join(data_dir,'cloud.png')).convert()
expsound=pygame.mixer.Sound(path.join(data_dir,'exp.wav'))
crashsound=pygame.mixer.Sound(path.join(data_dir,'crash.ogg'))
deadsound=pygame.mixer.Sound(path.join(data_dir,'dead.ogg'))
pygame.mixer.music.load(path.join(data_dir,'bgm.ogg'))
back_rect=back_img.get_rect()
exp=[]
for load in range(1,9):
	exp_img=pygame.image.load(path.join(data_dir,'bubble_explo{}.png'.format(load))).convert()
	exp_img.set_colorkey((0,0,0))
	exp.append(exp_img)

class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(cloud_img,(100,100))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.x=random.randint(-100,WIDTH)
	def update(self):
		self.rect.y+=1

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(player_img,(50,50))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.y=HEIGHT-40
		self.radius=1
		self.hp=100
		self.lives=2
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
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(enemy_img,(40,40))
		self.image.set_colorkey((255,255,255))
		self.rect=self.image.get_rect()
		self.Velocity=random.randint(1,3)
		self.rect.x=random.randint(0,WIDTH-40)
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

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image=exp[0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.last_time=0
	def update(self):
		now=pygame.time.get_ticks()
		if now-self.last_time>100:
			if self.frame<len(exp):
				self.image=exp[self.frame]
				self.frame+=1
				self.last_time=pygame.time.get_ticks()
			else:
				self.kill()

pygame.mouse.set_visible(0)
FPS=pygame.time.Clock()
player=Player()
clouds=pygame.sprite.Group()
enemys=pygame.sprite.Group()
bullets=pygame.sprite.Group()
exps=pygame.sprite.Group()

score=2019
game_run=True
lasttime=0
fire=-1

def draw_ui():
	txt="Score: {}".format(score)
	font_name=pygame.font.match_font('Times New Roman')
	font=pygame.font.Font(font_name,20)
	text_surface=font.render(txt,True,(255,255,255))
	text_rect=text_surface.get_rect()
	text_rect.x=WIDTH-100
	text_rect.y=15
	screen.blit(text_surface,text_rect)
	pygame.draw.rect(screen,(0,255,0),(10,15,player.hp,15))
	pygame.draw.rect(screen,(255,255,255),(10,15,100,15),2)
	for i in range(0,player.lives):
		pygame.draw.rect(screen,(0,0,255),(30*i+15,40,20,20))

pygame.mixer.music.play(loops=-1)
while game_run:
	FPS.tick(60)
	positionx=player.rect.centerx
	positiony=player.rect.centery
	screen.blit(back_img,back_rect)
	clouds.draw(screen)
	screen.blit(player.image,player.rect)
	enemys.draw(screen)
	bullets.draw(screen)
	exps.draw(screen)
	draw_ui()
	enemys.update()
	clouds.update()
	player.update()
	bullets.update()
	exps.update()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			exit(0)
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				fire=-fire
			if event.key==pygame.K_ESCAPE:
				exit(0)			
	enemyspawn=random.randint(1,201)
	if enemyspawn%15==0:
		enemy=Enemy()
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
	collision=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)
	if collision:
		crashsound.play()
		player.hp-=20
		if player.hp<5:
			deadsound.play()
			player.lives-=1
			player.hp=100
			if player.lives<0:
				game_run=False
	hits=pygame.sprite.groupcollide(bullets,enemys,True,True)		
	if hits:
		score+=1
		expsound.play()
	for hit in hits:
		exp_a=Explosion(hit.rect.center)
		exps.add(exp_a)
	pygame.display.flip()

while 1:
	screen.fill((0,0,0))
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