import pygame
from random import randint
from time import sleep

class AirGame:
    """A class representing an air game"""
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        #screen
        self.W, self.H = 600, 600
        self.screen = pygame.display.set_mode((self.W, self.H))
        #fps
        self.fps = 60
        self.clock = pygame.time.Clock()
        #background images
        self.background_image_of_menu = pygame.transform.scale(pygame.image.load('sources/images/air/air_menu.png').convert_alpha(), (self.W, self.H))
        self.background_image_of_game = pygame.transform.scale(pygame.image.load('sources/images/air/air_background.png').convert_alpha(), (self.W, self.H))
        self.background_x = 0
        #game variables
        self.flying = False
        self.game_over = False
        self.game_win = False
        #clouds
        self.clouds_width,self.clouds_height = 200,150
        self.speed_clouds = 4
        self.clouds_frequency = 1500
        self.last_cloud_time = pygame.time.get_ticks() - self.clouds_frequency #time for first cloud spawn
        self.clouds_position_x = self.W+150
        self.clouds_position_y = None
        #runes
        self.runes_width,self.runes_height = 50,50
        self.speed_runes = 4
        self.rune_frequency = None #random miliseconds for rune spawn
        self.last_rune_time = pygame.time.get_ticks() #time for first rune spawn
        self.last_collected_run_time = 0
        self.runes_collection = 0
        self.runes_collected_list = [] #list for detected runes
        self.rune_index = None #index of the rune image
        self.runes_position_x = self.W+150
        self.runes_position_y = None
        self.runes_name = ['fire', 'water', 'earth', 'air', 'light', 'dark', 'life']
        #player
        self.player = self.Player(self,100, self.H//2,self.H)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.clouds_group = pygame.sprite.Group()
        self.runes_group = pygame.sprite.Group()
        #fonts
        self.number_of_runes_font = pygame.font.Font('sources/fonts/air_font.ttf',25) 
        self.collected_rune_font = pygame.font.Font('sources/fonts/air_font.ttf',18)
        self.win_font = pygame.font.Font('sources/fonts/air_font.ttf',35) 
        self.win_font2 = pygame.font.Font('sources/fonts/air_font.ttf',18)
        self.lose_font = pygame.font.Font('sources/fonts/air_font.ttf',35) 
        #is_passed
        self.running = True
        self.solved = False
    
    class Player(pygame.sprite.Sprite):
        """A class representing the player"""
        def __init__(self,game_instance, x, y,H):
            """
            
            """
            super().__init__()
            self.game_instance = game_instance
            self.images = []
            self.index = 0
            self.counter = 0
            self.H = H
            for i in range(3):
                img = pygame.transform.scale(pygame.image.load(f'sources/images/air/player{i}.png').convert_alpha(), (75, 70))
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
            self.velocity = 0

        def update(self):
            """Update the player's position and animation"""
            if not self.game_instance.game_over:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] and self.rect.top - 35 > 0:
                    self.velocity = -6.5
            if self.game_instance.flying:
                self.velocity += 0.5
                if self.velocity > 8:
                    self.velocity = 8
                self.rect.y += int(self.velocity)
                if self.game_instance.flying:
                    COOLDOWN = 10
                    self.counter += 1
                    if self.counter > COOLDOWN:
                        self.counter = 0
                        self.index += 1
                        if self.index >= len(self.images):
                            self.index = 0
                    self.image = self.images[self.index]
                    self.image = pygame.transform.rotate(self.image, self.velocity*-1)
                    self.mask = pygame.mask.from_surface(self.image)

    class Cloud(pygame.sprite.Sprite):
        """A class representing a cloud"""
        def __init__(self,game_instance, x, y, index):
            super().__init__()
            self.game_instance = game_instance
            self.image = pygame.transform.scale(pygame.image.load(f'sources/images/air/cloud{index}.png').convert_alpha(), (200, 150))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
            self.speed_clouds = self.game_instance.speed_clouds

        def update(self):
            """Update the cloud position"""
            self.rect.x -= self.speed_clouds
            if self.rect.right < 0:
                self.kill()
                self.game_instance.speed_clouds += 0.01

    class Rune(pygame.sprite.Sprite):
        """A class representing a rune"""
        def __init__(self,game_instance, x, y, index):
            super().__init__()
            self.game_instance = game_instance
            self.index = index
            self.image = pygame.transform.scale(pygame.image.load(f'sources/images/air/rune{index}.png').convert_alpha(), (50, 50))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed_runes = self.game_instance.speed_runes

        def update(self):
            """Update the rune position"""
            self.rect.x -= self.speed_runes
            if self.rect.right < 0:
                self.kill()
    
    def game_over_menu(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound(('sources/sounds/air/lose_menu.mp3')).play(1)
        self.screen.fill('Black')
        self.lose_text = self.lose_font.render('You almost there',False,'SkyBlue')
        self.current_score = self.number_of_runes_font.render(f'Your score: {self.runes_collection}',False,'SkyBlue')
        self.screen.blit(self.lose_text,(self.W//2-180,250))
        self.screen.blit(self.current_score,(self.W//2-100,320))
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.mixer.stop()
        return None
     
    def win_game_menu(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound(('sources/sounds/air/win_menu.mp3')).play(1)
        self.screen.fill('Black')
        self.win_text = self.win_font.render('Congratulations!',False,'Gold')
        self.win_text2 = self.win_font2.render('You have mastered the air',False,'Gold')
        self.screen.blit(self.win_text,(self.W//2-180,250))
        self.screen.blit(self.win_text2,(self.W//2-150,320))
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.mixer.stop()
        return None
    
    def updating_groups(self):
        self.player_group.draw(self.screen)
        self.player_group.update()
        self.clouds_group.draw(self.screen)
        self.clouds_group.update()
        self.runes_group.draw(self.screen)
        self.runes_group.update()
    
    def collision_check(self):
        #mask collision
        if pygame.sprite.spritecollide(self.player,self.clouds_group,False,pygame.sprite.collide_mask): #collision with clouds
            self.game_over = True 
        if pygame.sprite.spritecollide(self.player,self.runes_group,True,pygame.sprite.collide_mask): #collision with runes
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sources/sounds/air/collected_rune.mp3'), maxtime=500) #catch the rune
            self.runes_collection += 1
            self.runes_collected_list.append(self.rune_index) #adding the index of which rune was collected
            self.last_collected_run_time = 35
        #checking for not be on top of each other
        if len(self.runes_group) > 0:
            for rune in self.runes_group:
                if pygame.sprite.spritecollide(rune,self.clouds_group,True,pygame.sprite.collide_mask): #deleting the cloud if collided with rune
                    pass
        #check if hit the ground
        if self.player.rect.bottom >= self.H: 
            self.game_over = True #lose
            self.flying = False
    
    def run_game(self):
        """Run the game"""
        self.running = True
        while self.running:
            if self.game_over == False and self.game_win == False:
                self.screen.blit(self.background_image_of_game, (self.background_x, 0))
                self.screen.blit(self.background_image_of_game, (self.background_x+600, 0))
                if self.flying == True:
                    self.background_x -= 1
                    if self.background_x <= -600:
                        self.background_x = 0
                #updating groups
                self.updating_groups()
                #collected runes text
                self.number_of_runes_text = self.number_of_runes_font.render(f'Collected runes: {self.runes_collection}',False,'Green') #collected runes text
                self.screen.blit(self.number_of_runes_text,(self.W//2-300//2,10))
                #collision check
                self.collision_check()
                #spawn clouds and runes
                if self.flying == True:
                    time_now = pygame.time.get_ticks()
                    #cloud spawn
                    if time_now - self.last_cloud_time > self.clouds_frequency:
                        self.clouds_position_y = randint(0,self.H-self.clouds_height)
                        cloud = self.Cloud(self,self.clouds_position_x,self.clouds_position_y,randint(0,4))
                        self.clouds_group.add(cloud)
                        self.last_cloud_time = time_now 
                    #runes spawn
                    self.rune_frequency = randint(7000,10000)
                    if time_now - self.last_rune_time > self.rune_frequency:
                        self.rune_index = randint(0,6)
                        self.runes_position_y = randint(0,self.H-self.runes_height)
                        if self.rune_index not in self.runes_collected_list: 
                            rune = self.Rune(self,self.runes_position_x,self.runes_position_y,self.rune_index)
                            self.runes_group.add(rune)
                            self.last_rune_time = time_now
                    if self.last_collected_run_time > 0:
                        self.last_collected_run_time -= 1
                        self.collected_rune_text = self.collected_rune_font.render(f'Collected rune {self.runes_name[self.rune_index]}',False,'Yellow') #collected rune text
                        self.screen.blit(self.collected_rune_text,(self.W-250,60))
                #win game
                if self.runes_collection == 7:
                    self.game_win = True
                    self.flying = False
            if self.game_over == True:
                self.game_over = False
                self.ruunning = False
                self.game_over_menu()
                self.solved = False
                return self.solved
            if self.game_win == True:
                self.game_win = False
                self.running = False
                self.win_game_menu()
                self.solved = True
                return self.solved
            pygame.display.flip()
            self.clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.passed = False
                    return self.passed
                if event.type == pygame.KEYDOWN and self.flying == False and self.game_over == False:
                    if event.key == pygame.K_SPACE:
                        self.flying = True
                        #music
                        self.music = pygame.mixer.music.load('sources/sounds/air/air.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.2)  
    def draw_menu(self):
        """Draw the menu screen"""
        self.screen.blit(self.background_image_of_menu, (0, 0))
        pygame.display.flip()

    def handle_menu(self):
        """Handle menu input"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
            
        return None

    def start(self):
        """Start the game"""
        self.running = True
        pygame.mixer.music.load('sources/sounds/air/air_menu.mp3')
        pygame.mixer.music.play(1)
        while self.running:
            menu_input = self.handle_menu()
            if menu_input is not None:
                if menu_input:
                    self.running = False
                else:
                    pygame.quit()
                    return

            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.mixer.music.stop()
        self.solved = self.run_game()
        return self.solved
    
#start game
if __name__ == "__main__":
    game = AirGame()
    game.start()
