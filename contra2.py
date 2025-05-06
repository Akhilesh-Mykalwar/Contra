import pygame
import os
import pygame, sys
from pygame.locals import *
import random
import csv
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


#set framerate
clock = pygame.time.Clock()
FPS = 60


scroll_thresh = 200
screen_scroll = 0
bg_scroll = 0
GRAV = 0.75
ROWS = 16
COLS = 150
tile = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
#define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

img_list = []
for i in range(TILE_TYPES):
	img = pygame.image.load(f"C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\tiles\\{i}.png")
	img = pygame.transform.scale(img,(tile,tile))
	img_list.append(img)
bullet_img = pygame.image.load("C:\\Users\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\bullet.png").convert_alpha()

bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * 4), int(bullet_img.get_height() * 4))).convert_alpha()

pine1_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\pine1.png").convert_alpha()

pine2_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\pine2.png").convert_alpha()

mountain_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\mountain.png").convert_alpha()

sky_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\sky_cloud.png").convert_alpha()



health_box_img = pygame.image.load("C:\\Users\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\health_box.png").convert_alpha()

ammo_box_img = pygame.image.load("C:\\Users\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\ammo.png").convert_alpha()

grenade_box_img = pygame.image.load("C:\\Users\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\grenade_box.png").convert_alpha()

item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
	'Grenade'	: grenade_box_img	
}

grenade_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\Grenade1.png").convert_alpha()


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)



font = pygame.font.SysFont('Futura',40)


def draw_text(text, font , col, x, y):
	img = font.render(text, True, col)
	screen.blit(img ,(x,y))

def draw_bg():
	screen.fill(BG)
	screen.blit(sky_img,(0,0))
	screen.blit(mountain_img, (0, SCREEN_HEIGHT - mountain_img.get_height() - 300))
	screen.blit(pine1_img, (0, SCREEN_HEIGHT - pine1_img.get_height() - 150))
	screen.blit(pine2_img,(0,SCREEN_HEIGHT - pine2_img.get_height()))

class Soldier(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed , ammo , grenades):
		pygame.sprite.Sprite.__init__(self)

		self.char_type = char_type
		self.speed = speed
		self.life = True
		self.action = 0
		self.direction = 1
		self.flip = False
		self.grenades = grenades
		self.vely = 0
		self.action = 0
		self.airtime = True
		self.shoot_cd = 0
		self.ammo = ammo
		self.start_ammo = ammo		
		self.health = 100
		self.max_health = 100
		self.jump = False
		self.animation = []
		idle = []
		run = []
		temp = []
		self.index = 0
		self.update_time = pygame.time.get_ticks()
		#AI
		self.vision = pygame.Rect(0, 0, 150,20)
		self.move_counter = 0
		self.idle = False
		self.idling = 0
		for i in range (1,5):
			img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\{char_type}\\{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			temp.append(img)
		self.animation.append(temp)

		temp = []
		
		for i in range (1,7):
			img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\{char_type}\\run{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			temp.append(img)
		
		self.animation.append(temp)

		temp = []

		for i in range (1,3):
			img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\{char_type}\\jump{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			temp.append(img)
		
		self.animation.append(temp)

		temp = []

		for i in range (0,6):
			img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\{char_type}\\death{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			temp.append(img)
		
		self.animation.append(temp)

		


		self.image = self.animation[self.action][self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


		self.width = self.image.get_width()
		self.height = self.image.get_height()

	
	def update(self):
		self.update_animation()
		self.check_alive()

		if self.shoot_cd > 0:

			self.shoot_cd -= 1

		
	
		

	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0
		dx = 0
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1

		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		if self.jump  == True and self.airtime == False:
			self.vely = -11
			self.jump = False
			self.airtime = True

		self.vely += GRAV
		if self.vely > 10:
			self.vely
		dy += self.vely


		

		


		for Tile in world.obstacle_list:
			if Tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width, self.height):
				dx = 0
				if self.char_type == 'enemy':
					self.direction *= -1
					self.move_counter = 0
			if Tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height):

				if self.vely < 0 :
					self.vely = 0
					dy = Tile[1].bottom - self.rect.top


				elif self.vely >= 0:
					self.vely = 0
					self.airtime = False
					dy = Tile[1].top - self.rect.bottom
		#update rectangle position
		if self.char_type == 'player':
			if self.rect.left + dx < 0 or self.rect.right > SCREEN_WIDTH:
				dx = 0			

		self.rect.x += dx
		self.rect.y += dy

		if self.char_type == 'player':

			if (self.rect.right > SCREEN_WIDTH - scroll_thresh and bg_scroll < (world.level_length * tile) - SCREEN_WIDTH) or (self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
				self.rect.x -= dx
				screen_scroll -= dx 
		return screen_scroll
	
	
		
	def shoot(self):
		if self.shoot_cd == 0 and self.ammo > 0:

			self.shoot_cd = 20
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			self.ammo -= 1
			



	


	def ai(self):
		

		
		if self.life and player.life:


			if self.idle == False and random.randint(1,250) == 1:
				self.update_action(0)
				self.idle = True
				self.idling = 250
					

			if self.vision.colliderect(player.rect):
				self.update_action(0)
				self.shoot()
			else:

				
				if self.idle == False:
					

					if self.direction == 1:
						ai_moving_right = True
					else:
						ai_moving_right = False
					ai_moving_left = not ai_moving_right
					self.move(ai_moving_left, ai_moving_right)
					self.update_action(1)
					self.move_counter += 1

					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
					

					if self.move_counter > tile :
						self.direction *= -1
						self.move_counter *= -1

				else:
					self.idling -= 1
					if self.idling <= 0:
						self.idle = False
		
		self.rect.x += screen_scroll
		
	def update_animation(self):
		CD = 100
		self.image = self.animation[self.action][(self.index)]
		if pygame.time.get_ticks() - self.update_time > CD:
			self.update_time = pygame.time.get_ticks()
			self.index += 1
			if self.index >= len(self.animation[self.action] ):

				if self.action == 3:
					self.index = len(self.animation[self.action] ) - 1
				else :
					self.index = 0


	def update_action(self,new):
		if new != self.action:
			self.action = new
			self.index = 0
			self.update_time = pygame.time.get_ticks()


	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.life = False
			self.update_action(3)


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
		




class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):

		self.level_length = len(data[0])


		for y,row in enumerate(data):

			for x,Tile in enumerate(row):
				if Tile >= 0:
					img = img_list[Tile]
					img_rect = img.get_rect()
					img_rect.x = x * tile
					img_rect.y = y * tile

					tile_data = (img, img_rect)
					if Tile >= 0 and Tile <= 8:
						self.obstacle_list.append(tile_data)

					elif Tile >= 9 and Tile <= 10:
						water = Water(img, x * tile, y * tile)
						Water_group.add(water)

					elif Tile >= 11 and Tile <= 14:
						decoration = Decoration(img, x * tile, y * tile)
						Decoration_group.add(decoration)

					elif Tile == 15:
						player = Soldier('soldier', x * tile, y * tile, 1.65, 5 , 20 , 5)
						hp_bar = HealthBar(10 ,10,player.health,player.health)
	
					elif Tile == 16:
						enemy = Soldier('enemy', x * tile, y * tile, 1.65, 2, 20, 0)
						enemy_group.add(enemy)
	
					elif Tile == 17:
						item_box = ItemBox('Ammo', x * tile, y * tile)
						item_box_group.add(item_box)
					elif Tile == 18:
						item_box = ItemBox('Grenade', x * tile, y * tile)
						item_box_group.add(item_box)
					elif Tile == 19:
						item_box = ItemBox('Health', x * tile, y * tile)
						item_box_group.add(item_box)
					elif Tile == 20:
						exit = Exit(img, x * tile, y * tile)
						Exit_group.add(exit)

		return player, hp_bar			

	def draw(self):
		for Tile in self.obstacle_list:
			Tile[1][0] += screen_scroll
			screen.blit(Tile[0],Tile[1])



class Grenade(pygame.sprite.Sprite):
	def __init__(self,x,y,direction):
		pygame.sprite.Sprite.__init__(self)
		self.timer = 100
		self.vely = -11
		self.speed = 8
		self.image = grenade_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction
		self.height = self.image.get_height()
		self.width = self.image.get_width()


	def update(self):
		self.vely += GRAV
		dx = self.speed * self.direction
		dy = self.vely


		for Tile in world.obstacle_list:

			if Tile[1].colliderect(self.rect.x + dx,self.rect.y,self.width,self.height):
				self.direction *= -1
				dx = self.speed * self.direction
				
					

			if Tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height):
				self.speed = 0
				if self.vely < 0 :
					self.vely = 0
					dy = Tile[1].bottom - self.rect.top


				elif self.vely >= 0:
					self.vely = 0
					
					dy = Tile[1].top - self.rect.bottom
			

		 

		
		self.rect.x += dx + screen_scroll
		self.rect.y += dy

		self.timer -= 1
		if self.timer <= 0:
			self.kill()
			exp = Explosion(self.rect.x , self.rect.y , 1)
			Explosion_group.add(exp)
			if abs(self.rect.centerx - player.rect.centerx) < tile * 2 and abs(self.rect.centery - player.rect.centery) < tile * 3 :
				player.health -= 60
									
			for enemy in enemy_group:			     
				if abs(self.rect.centerx - enemy.rect.centerx) < tile * 3 and abs(self.rect.centery - enemy.rect.centery) < tile * 3 :
				 enemy.health -= 100

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, Direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 20
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.Direction = Direction


	def update(self):
		#move bullet
		self.rect.x += (self.Direction * self.speed) + screen_scroll
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		#check for collision with level
		for Tile in world.obstacle_list:
			if Tile[1].colliderect(self.rect):
				self.kill()

		#check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 10
				self.kill()
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					self.kill()



class Explosion(pygame.sprite.Sprite):
	def __init__(self,x,y,scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1,6):
			img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\assets\\exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale ), int(img.get_height() * scale)))
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0



	def update(self):

		self.rect.x += screen_scroll
		EXP_SPEED = 4
		self.counter += 1

		if self.counter >= EXP_SPEED:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
				self.kill()
			else:

				self.image = self.images[int(self.index)]			


class Decoration(pygame.sprite.Sprite):

	def __init__(self,img,x,y):

		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()

		self.rect.midtop = (x + tile // 2, y + (tile - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):

	def __init__(self,img,x,y):

		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()

		self.rect.midtop = (x + tile // 2, y + (tile - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self,img,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()

		self.rect.midtop = (x + tile // 2, y + (tile - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll



class ItemBox(pygame.sprite.Sprite):
	def __init__(self,item_type,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile // 2 , y + (tile - self.image.get_height()))

	def update(self):
		
		self.rect.x += screen_scroll

		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			elif self.item_type == 'Grenade':
				player.grenades += 3
			#delete the item box
			self.kill()
			
		
class HealthBar():

	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health


	def draw(self, health):
		self.health = health
		ratio = self.health / self.max_health
		pygame.draw.rect(screen,BLACK,(self.x - 2,self.y - 2,154,24))
		pygame.draw.rect(screen,RED,(self.x,self.y,150,20))
		pygame.draw.rect(screen,GREEN,(self.x,self.y,150 * ratio,20))



		

bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
Explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

Decoration_group = pygame.sprite.Group()
Water_group = pygame.sprite.Group()
Exit_group = pygame.sprite.Group()




world_data = []
for row in range (ROWS):
	r = [-1] * COLS
	world_data.append(r)

with open(f'level{level}_data.csv',newline='') as csvfile:

	reader = csv.reader(csvfile, delimiter=',')
	for x,row in enumerate(reader):

		for y,Tile in enumerate (row):

			world_data[x][y] = int(Tile)

world = World()
player, hp_bar = world.process_data(world_data)

run = True

while run:

	clock.tick(FPS)

	draw_bg()

	world.draw()


	hp_bar.draw(player.health)

	draw_text(f'Ammo: ',font, WHITE,10, 35)
	for x in range(player.ammo):
		screen.blit(bullet_img, (90 + (x*10),45))

	draw_text(f'GRENADES: ',font, WHITE,10, 60)
	for x in range(player.grenades):
		screen.blit(grenade_img, (135 + (x * 15),60))
	
	
	
	player.update()

	player.draw()

	for enemy in enemy_group:
		enemy.ai()
		enemy.update()
		enemy.draw()


	bullet_group.update()
	grenade_group.update()
	bullet_group.draw(screen)
	grenade_group.draw(screen)
	Explosion_group.update()
	Explosion_group.draw(screen)
	item_box_group.draw(screen)
	item_box_group.update()
	
	Decoration_group.update()
	
	Water_group.update()
	Exit_group.update()
	Decoration_group.draw(screen)
	Water_group.draw(screen)
	Exit_group.draw(screen)

	if player.life == True:

		if shoot :
			player.shoot()

		elif grenade and grenade_thrown == False and player.grenades > 0:
			grenade = Grenade(player.rect.centerx + 0.4 * (player.rect.size[0] * player.direction), player.rect.top * 1.1, player.direction)
			grenade_group.add(grenade)
			player.grenades -= 1

			grenade_thrown = True
		if player.airtime :
			player.update_action(2)


		elif moving_left or moving_right:
			

			player.update_action(1)
		

		else:

			player.update_action(0)

		screen_scroll = player.move(moving_left, moving_right)
		
		bg_scroll -= screen_scroll
	   
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.MOUSEBUTTONDOWN:
			shoot = True
		if event.type == pygame.KEYDOWN and player.life:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_w and player.life:
				player.jump = True
			if event.key == pygame.K_SPACE:
				grenade = True
				
		if event.type == pygame.MOUSEBUTTONUP:
			shoot = False

		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				grenade = False
				grenade_thrown = False




	pygame.display.update()

pygame.quit()