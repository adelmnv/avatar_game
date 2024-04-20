import pygame
from random import randint

#initializing pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
#classes
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] #list of images for animation
        self.index = 0 #index of the image
        self.counter = 0 # counter for animation
        for i in range(3):
            img = pygame.transform.scale(pygame.image.load(f'sources/images/air/player{i}.png').convert_alpha(),(75,70))
            self.images.append(img) #adding images to the list
        self.image = self.images[self.index] #current image
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.mask = pygame.mask.from_surface(self.image) #mask for collision
        self.velocity = 0 #gravitation speed
        self.clicked = False # mouse click for jump
        
    def update(self):
        if flying:    #gravitation
            self.velocity += 0.5 #gravitation speed
            if self.velocity > 9:
                self.velocity = 9 #resetting the velocity
            if self.rect.bottom < H:
                self.rect.y += int(self.velocity) # always falling
        if not game_over:  #jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.rect.top-self.rect.height+6 > 0:
                self.clicked = True
                self.velocity = -9 #jumping speed
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            #image animation
            if flying:
                COOLDOWN = 10 #animation changing speed
                self.counter += 1
                if self.counter > COOLDOWN: #interval for changing the image
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index] #changing the image
                #rotating when flying
                self.image = pygame.transform.rotate(self.image, self.velocity*-1)
  
class Clouds(pygame.sprite.Sprite):
    def __init__(self,x,y,index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f'sources/images/air/cloud{index}.png').convert_alpha(),(200,150))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.mask = pygame.mask.from_surface(self.image) #mask for collision
        
    def update(self):
        self.rect.x -= speed_cloud #always moving to the left
        if self.rect.right < 0:
            self.kill() #removing if out of the screen
            
class Runes(pygame.sprite.Sprite):
    def __init__(self,x,y,index):
        pygame.sprite.Sprite.__init__(self)
        self.index = index #index of rune image
        self.image = pygame.transform.scale(pygame.image.load(f'sources/images/air/rune{index}.png').convert_alpha(),(50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
    def update(self):
        self.rect.x -= speed_runes #always moving to the left
        if self.rect.right < 0:
            self.kill() #removing if out of the screen

#screen
W,H = 600,600
screen = pygame.display.set_mode((W,H))
#FPS
fps = 60
clock = pygame.time.Clock()
#background image of menu
background_image_of_menu = pygame.transform.scale(pygame.image.load('sources/images/air/air_menu.jpg').convert_alpha(),(W,H))
#background image of game
background_image_of_game = pygame.transform.scale(pygame.image.load('sources/images/air/air_background.png').convert_alpha(),(W,H))
background_x = 0
#game variables
flying = False #game start
game_over = False
game_win = False

clouds_width,clouds_height = 200,150 #clouds size
speed_cloud = 4 #constant speed of cloud
clouds_frequency = 1500 #constant miliseconds for cloud spawn 
last_cloud_time = pygame.time.get_ticks() - clouds_frequency #time for first cloud spawn
clouds_position_x = W+100 #position spawn of clouds by x axis
clouds_position_y = None #position spawn ofclouds by y axis

runes_width,runes_height = 50,50 #runes size
speed_runes = 4 #constant speed of runes
rune_frequency = None #random miliseconds for rune spawn
last_rune_time = pygame.time.get_ticks() #time for first rune spawn
last_collected_run_time = 0 #last time for collected rune text
runes_collection = 0 # collected runes
runes_collected_list = [] # list for detected runes
rune_index = None # index of the rune image 
runes_position_x = W+100 # position spawn of runes by x axis
runes_position_y = None # position spawn of runes by y axis
runes_name = ['fire','water','earth','air','light','dark','life'] #names of the runes
#fonts
number_of_runes_font = pygame.font.Font('sources/fonts/rune_font.ttf',25) #font for collection of runes
collected_rune_font = pygame.font.Font('sources/fonts/rune_font.ttf',18) #font for collected runes
win_font = pygame.font.Font('sources/fonts/jersey10regular.ttf',100) #font for winnig menu
lose_font = pygame.font.Font('sources/fonts/jersey10regular.ttf',100) #font for losing menu
#music
music = pygame.mixer.music.load('sources/sounds/air/background_music.mp3')
pygame.mixer.music.play(-1) #infinity sound
pygame.mixer.music.set_volume(0.2) #volume

            
#player group
player_group = pygame.sprite.Group() 
player = Player(100,H//2)
player_group.add(player)
#clouds group
clouds_group = pygame.sprite.Group()
#runes group
runes_group = pygame.sprite.Group()
while True:
    if game_over == False and game_win == False:
        #background
        screen.blit(background_image_of_game, (background_x,0))
        screen.blit(background_image_of_game, (background_x+600,0))
        if flying:
            background_x -= 1
            if background_x <= -600:
                background_x = 0
        #player drawing
        player_group.draw(screen)
        player_group.update()
        #clouds drawing
        clouds_group.draw(screen)
        clouds_group.update()
        #runes drawing
        runes_group.draw(screen)
        runes_group.update()
        #collected runes text
        number_of_runes_text = number_of_runes_font.render(f'Collected runes: {runes_collection}',False,'Green') #collected runes text
        screen.blit(number_of_runes_text,(W//2-300//2,10))
        #mask collision
        if pygame.sprite.spritecollide(player,clouds_group,False,pygame.sprite.collide_mask): #collision with clouds
            game_over = True 
        if pygame.sprite.spritecollide(player,runes_group,True,pygame.sprite.collide_mask): #collision with runes
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sources/sounds/air/collected_rune.mp3'), maxtime=500) #catch the rune
            runes_collection += 1 # collected runes
            runes_collected_list.append(rune_index) #adding the index of which rune was collected
            last_collected_run_time = 35 #time for collected rune text
        #checking for not be on top of each other
        if len(runes_group) > 0:
            for rune in runes_group:
                if pygame.sprite.spritecollide(rune,clouds_group,True,pygame.sprite.collide_mask): #deleting the cloud if collided with rune
                    pass
        #check if hit the ground
        if player.rect.bottom >= H: 
            game_over = True #lose
            flying = False
        if flying == True:
            time_now = pygame.time.get_ticks()
            #cloud spawn
            if time_now - last_cloud_time > clouds_frequency: #checking the time for cloud spawn
                clouds_position_y = randint(0,H-clouds_height) #random position of y axis for cloud spawn
                cloud = Clouds(clouds_position_x,clouds_position_y,randint(0,4))
                clouds_group.add(cloud)
                last_cloud_time = pygame.time.get_ticks() #resetting the time
            #runes spawn
            rune_frequency = randint(4500,6000) #random time for rune spawn
            if time_now - last_rune_time > rune_frequency: #checking the time for rune spawn
                rune_index = randint(0,6) #random index of the rune image
                runes_position_y = randint(0,H-runes_height) #random position of y axis for rune spawn
                if rune_index not in runes_collected_list: 
                    rune = Runes(runes_position_x,runes_position_y,rune_index)
                    runes_group.add(rune)
                    last_rune_time = time_now
            print(time_now,last_rune_time)
            #
            if last_collected_run_time > 0:
                last_collected_run_time -= 1
                collected_rune_text = collected_rune_font.render(f'Collected rune {runes_name[rune_index]}',False,'Yellow') #collected rune text
                screen.blit(collected_rune_text,(W-250,60))
        if runes_collection == 7: #win game
            game_win = True
            flying = False
    
    #game win
    if game_win:
        screen.fill('Black')
        win_text = win_font.render('You Win',False,'Red') 
        current_runes = win_font.render(f'Collected runes {runes_collection}',False,'Purple')  
        screen.blit(win_text,(W//2-273//2,180))
    #game over
    if game_over:
        screen.fill('Black')
        lose_text = lose_font.render('You Lose',False,'Red')
        screen.blit(lose_text,(W//2-311//2,180))
        
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True   
    pygame.display.flip()
    clock.tick(fps)

