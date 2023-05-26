import pygame
import random
from pygame import mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#load sounds

flyFx = pygame.mixer.Sound('sounds/flap.mp3')
flyFx.set_volume(0.4)
passFx = pygame.mixer.Sound('sounds/point.mp3')
passFx.set_volume(0.4)
hitFx = pygame.mixer.Sound('sounds/hit.mp3')
hitFx.set_volume(0.4)

clock = pygame.time.Clock()
frames = 60

windowWidth = 838
windowHeight = 930
play = True

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Wing Jump')

#define font
font = pygame.font.SysFont("leelawadeeui", 45)



#define game variables
floorScroll = 0
speed = 6
flying = False
game_over = False
pipesSpread = 250
last_pipe_drawn = pygame.time.get_ticks() - 1600 #milliseconds
score = 0
handedOverPipe = 0

#load images
background = pygame.image.load('background.png')
floorImage = pygame.image.load('floor.png')
ButtonImageRestar = pygame.image.load('restart.png')
plagagainImageButton=pygame.image.load('playagain.png')









class Wingy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self) #spirit have draw and update functions built in
		self.images = []
		self.index = 0
		self.lives=3
		self.counter = 0

		img = pygame.image.load('flappybird.png')
		img2 = pygame.image.load('flappyBirdsecondpos.png')
		img3 = pygame.image.load('flappyBirdThirdPos.png')
		self.images.append(img)
		self.images.append(img2)
		self.images.append(img3)

		self.image = self.images[self.index] #get the image in index
		self.rect = self.image.get_rect()    #rectangle create rectangle from the image
		self.rect.center = [x, y]  #the position of rectangle
		self.vel = 0
		self.clicked = False   #setting value clicked false as default

	def update(self):

		if flying == True:
			#gravity
			self.vel += 0.5 # positv velocity moves the bird down as we're increasing the y
			if self.vel > 8:
				self.vel = 8 #setting the velocity as 8 maximmum
			if self.rect.bottom < 760:  #768 the bottom of the window
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False: #the second conditition to prevent holding in mouse
				self.clicked = True
				flyFx.play()
				self.vel = -10
			# the opposite of the condition  to allow user to perform more than one click
			if pygame.mouse.get_pressed()[0] == False:
				self.clicked = False

			#handle the animation
			self.counter += 1  # #increase it 1 each iteration
			fallsDown = 5

			if self.counter > fallsDown: # #if the counter greater than flap_cool start with next image
				self.counter = 0
				self.index += 1  #increae the index by 1 to move to next image
				if self.index >= len(self.images):  #check if the index greater than length of the list
					self.index = 0
			self.image = self.image  #set the image of index

			self.image = self.images[self.index]
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90) # if game is over rotate the bird 90 clockwise


class PAImageButton():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):

		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check if mouse is over the button
		if self.rect.collidepoint(pos):  # check if the mouse cursor inside the button image
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		window.blit(self.image, (self.rect.x, self.rect.y))

		return action


class Pipes(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('pipe.png')
		self.rect = self.image.get_rect()  #get the rectangel of that image
		#1 is from top -1 is bottom  these values to be multiplied by 90 degree
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True) # (img,x axis , y axis)
			self.rect.bottomleft = [x, y - int(pipesSpread / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipesSpread / 2)]

	def update(self):
		self.rect.x -= speed
		if self.rect.right < 0: #delete the pip when its close to 0 x axis set 200 to see difference
			self.kill() #delete the pipe


class restartButton():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):

		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check if mouse is over the button
		if self.rect.collidepoint(pos):  # check if the mouse cursor inside the button image
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		window.blit(self.image, (self.rect.x, self.rect.y))

		return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

birdy = Wingy(100, int(windowHeight / 2))

bird_group.add(birdy)

#create restart image button
button = restartButton(windowWidth // 2 - 50, windowHeight // 2 - 100, ButtonImageRestar)
replaybutoon=PAImageButton(windowWidth // 4, windowHeight // 2 + 100, plagagainImageButton)



def restart():
	pipe_group.empty()
	birdy.rect.x = 100
	birdy.rect.y = int(windowHeight / 2)
	score = 0
	birdy.lives=3

	return score


def replayAgain():

	pipe_group.empty()
	birdy.rect.x = 100
	birdy.rect.y = int(windowHeight / 2)
	birdy.lives-=1

while play==True:

	clock.tick(frames)

	#draw background
	window.blit(background, (0, 0))  # this method to show the image on the screen

	bird_group.draw(window)
	bird_group.update()
	pipe_group.draw(window)

	#draw the ground
	window.blit(floorImage, (floorScroll, 760))  # using the floor var to move the screen while the game is running
	if birdy.lives>0:
		if birdy.lives>=1:
			heartImage = pygame.image.load("pngwing.com.png")
			window.blit(heartImage,(0,0))

		if birdy.lives >=2:
			heartImage = pygame.image.load("pngwing.com.png")
			window.blit(heartImage, (60, 0))
		if birdy.lives >=3:
			heartImage = pygame.image.load("pngwing.com.png")
			window.blit(heartImage, (120, 0))
	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and handedOverPipe == False:
			handedOverPipe = True
		if handedOverPipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				passFx.play()
				handedOverPipe = False



	img = font.render("score :"+str(score), True, (0,0,0))
	window.blit(img, (windowWidth//2-100, 10))

	#check for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or birdy.rect.top < 0: # # false is do kill argument
		game_over = True
		hitFx.play()


	#check if bird has hit the ground
	if birdy.rect.bottom >= 760: #768 is the bottom of the screen
		game_over = True
		flying = False
		hitFx.play()



	if game_over == False and flying == True:

		#generate new pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe_drawn > 1600:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipes(windowWidth, int(windowHeight / 2) + pipe_height, position=-1) #generate pipe at the bottom
			top_pipe = Pipes(windowWidth, int(windowHeight / 2) + pipe_height, position= 1)  #generate another pipe at same x coordintae  but in the top
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe_drawn = time_now  #change the varible value of the current created pipe


		#draw and scroll the ground
		floorScroll -= speed
		if abs(floorScroll) > 35: #start new screen once the end of last screen reaches 35
			floorScroll = 0

		pipe_group.update()


	#check for game over and reset
	if game_over == True and birdy.lives==1:
		if button.draw() == True:
			game_over = False
			score = restart()

	elif game_over ==True and birdy.lives>0:

		if replaybutoon.draw() == True:
			game_over = False
			replayAgain()



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			play = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()