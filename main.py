import pygame
import random


pygame.init()

# เฟรมเรท
FPS = 30

# ปรับความกกว้าง-สูงของเกม 
WIDTH = 800
HEIGHT = 700

# คะแนน
SCORE = 0
# ชีวิต
LIVES = 3


BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

# สร้างสกรีน หรือ กล่องใส่เเกม
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# สร้างชื่อเกม
pygame.display.set_caption("My First Game by Jack")


# Background
bg = "C:\\Users\\User\\Desktop\\pygame\\First Game\\Background.png"
background = pygame.image.load(bg).convert_alpha()
background_rect = background.get_rect()


# สร้างนาฬิกาของเกม
clock = pygame.time.Clock()




class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		img = "C:\\Users\\User\\Desktop\\pygame\\First Game\\bomber.png"
		self.image = pygame.image.load(img).convert_alpha()

		# self.image = pygame.Surface((50,50))
		# self.image.fill(GREEN)

		# สร้างสี่เเหลี่ยม
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT - self.rect.height)

		# speed x
		self.speed_x = 0



	def update(self):
		#self.rect.y += 5
		self.speed_x = 0
		# เช็คว่ามีการกดปุ่มหรอไม่
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5

		self.rect.x += self.speed_x


		if self.rect.bottom > HEIGHT:
			self.rect.y = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		group_bullet.add(bullet)


class Bullet(pygame.sprite.Sprite):

	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((10,10))
		self.image.fill(GREEN)

		# สร้างสี่เเหลี่ยม
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

		# speed x
		self.speed_y = -10

	def update(self):
		self.rect.y += self.speed_y

		# ลบกระสุนเมื่อ แกน y < 0
		if self.rect.y < 0:
			self.kill()


class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		img = "C:\\Users\\User\\Desktop\\pygame\\First Game\\aircraft.png"
		self.image = pygame.image.load(img).convert_alpha()

		# self.image = pygame.Surface((50,50))
		# self.image.fill(GREEN)

		# สร้างสี่เเหลี่ยม
		self.rect = self.image.get_rect()

		# สุุ่มตำแหน่งแนวแกน x
		rand_x = random.randint(self.rect.width,WIDTH - self.rect.width)
		self.rect.center = (rand_x, 0)

		# speed y
		self.speed_y = random.randint(1,10)


	def update(self):
		self.rect.y += self.speed_y
		if self.rect.bottom > HEIGHT:
			self.rect.y = 0
			rand_x = random.randint(self.rect.width,WIDTH - self.rect.width)
			self.rect.x = rand_x
			self.speed_y = random.randint(1,10)

font_name = pygame.font.match_font("arial")

def draw_text(screen,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.topleft = (x,y)
	screen.blit(text_surface, text_rect)


# draw_text(screen, "SCORE:100", 30, WIDTH-100, 10)


# สร้างกลุ่ม Sprite
all_sprites = pygame.sprite.Group()
group_enemy = pygame.sprite.Group() #กล่องสำหรับเก็บ enemy
group_bullet = pygame.sprite.Group() # กล่องสำหรับใส่ กระสุน

# player
player = Player()
all_sprites.add(player)

# enemy
for i in range(5):
	enemy = Enemy()
	all_sprites.add(enemy)
	group_enemy.add(enemy)



# สถานะของเกม
running = True

while running:

	# สั่งให้เกมรันตามเฟรมเรท
	clock.tick(FPS)

	# ตรวจสอบว่าปิดเกมยัง
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()



	all_sprites.update()

	# ตรวจสอบการชนกันของ sprites กับ enemy
	collide = pygame.sprite.spritecollide(player, group_enemy, False)
	#print(collide)

	



	if collide:
		# หากมีการชนกัน  จะปืดโปรแแกรมทันที
		running = False


	# bullet collide
	hits = pygame.sprite.groupcollide(group_bullet, group_enemy, True, True)
	#print(hits)
	for h in hits:
		enemy = Enemy()
		all_sprites.add(enemy)
		group_enemy.add(enemy)

		# add score
		SCORE += 10

	
	# ใส่สีแบคกกราวของเกม
	screen.fill(BLACK)

	screen.blit(background,background_rect)

	draw_text(screen, "SCORE: {}".format(SCORE), 30, WIDTH-200, 10)
	draw_text(screen, "LIVES: {}".format(LIVES), 20, 100, 10)

	# นำตัวละครทั้งหมดดมาวาดใส่เกม
	all_sprites.draw(screen)


	pygame.display.flip()  # ทำให้ pygame แสดงผล


pygame.quit() # ออกจากเกมS