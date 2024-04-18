import pygame
import sys
import os
import random

class ArrowsGame:
    def __init__(self):
        pygame.init()

        # Size of the window
        self.WIDTH, self.HEIGHT = 600, 600

        # Initializing the window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Fire - The Dancing Dragon")

        # Loading images
        self.arrow_images = {
            'up': pygame.image.load("sources/images/fire/arrow_up.jpeg"),
            'down': pygame.image.load("sources/images/fire/arrow_down.jpeg"),
            'left': pygame.image.load("sources/images/fire/arrow_left.jpeg"),
            'right': pygame.image.load("sources/images/fire/arrow_right.jpeg"),
            'standard': pygame.image.load("sources/images/fire/arrow_standard.jpeg"),
            'standard_dark': pygame.image.load("sources/images/fire/arrow_standard_dark.jpeg")
        }

        for key in self.arrow_images:
            self.arrow_images[key] = pygame.transform.scale(self.arrow_images[key], (600, 600))
        
        #self.message_background = pygame.transform.scale(pygame.image.load("sources/images/arrow_up.jpeg"), (400, 100))
        
        pygame.mixer.music.load('sources/sounds/fire/dragon_dance_v2.mp3')

        self.running = True

        self.count = 2

    def _generate_combination(self):
        arrows = ['up', 'down', 'left', 'right']
        return [random.choice(arrows) for _ in range(self.count)]

    def _display_message(self, message):
        self.screen.blit(self.arrow_images['standard_dark'], (0, 0))
        font = pygame.font.SysFont('Papyrus', 36)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        background_rect = text_rect.inflate(80, 40)  #Enlarging the rectangle for filling
        pygame.draw.rect(self.screen, (219, 193, 109), background_rect)
        self.screen.blit(text, text_rect)
        pygame.display.update() 
        pygame.time.delay(1000) 

    def _display_combination(self, combination):
        self.screen.blit(self.arrow_images['standard'], (0, 0))
        pygame.display.update()  
        pygame.time.delay(1000)  
        
        for arrow in combination:
            pygame.mixer.Sound('sources/sounds/fire/fire_sound.mp3').play()
            self.screen.blit(self.arrow_images[arrow], (0, 0))
            pygame.display.update()  
            pygame.time.delay(1000) 
            self.screen.blit(self.arrow_images['standard'], (0, 0))
            pygame.display.update()  
            pygame.time.delay(500)  

    def run(self):
        pygame.mixer.music.play(-1)
        while self.running:
            self._display_message("Remember the combination")
            combination = self._generate_combination()  # Arrow's combination generation
            self._display_combination(combination)  # Display of arrow combination

            input_complete = False
            user_input = []
            self._display_message("Your turn")
            pygame.time.delay(200)  
            self.screen.blit(self.arrow_images['standard'], (0, 0))
            pygame.display.update()

            while not input_complete:
                arrow = ''
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            user_input.append('up')
                            arrow = 'up'
                        elif event.key == pygame.K_DOWN:
                            user_input.append('down')
                            arrow = 'down'
                        elif event.key == pygame.K_LEFT:
                            user_input.append('left')
                            arrow = 'left'
                        elif event.key == pygame.K_RIGHT:
                            user_input.append('right')
                            arrow = 'right'
                        elif event.key == pygame.K_RETURN:
                            input_complete = True
                    elif event.type == pygame.QUIT:
                        self.running = False
                if arrow:  # Checking if an arrow was pressed
                    pygame.mixer.Sound('sources/sounds/fire/fire_sound.mp3').play()
                    self.screen.blit(self.arrow_images[arrow], (0,0))
                    pygame.display.update()
                    pygame.time.delay(500) 
                    self.screen.blit(self.arrow_images['standard'], (0, 0))
                    pygame.display.update()  
            
            # Checking user input
            if user_input == combination:
                # Checking if game is completed
                if self.count == 5:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound('sources/sounds/fire/dragon_dance_win.mp3').play()
                    self._display_message("You've managed to master fire!")
                    pygame.time.delay(1000)
                    pygame.mixer.music.stop()
                    self.running = False
                else:
                    self._display_message("Right. Go on...")
                    self.count += 1
            else:
                pygame.mixer.music.stop()
                pygame.mixer.Sound('sources/sounds/fire/dragon_dance_loose.mp3').play()
                self._display_message("Wrong, you haven't mastered fire.")
                pygame.time.delay(1000)
                pygame.mixer.music.stop()
                self.running = False
                    



if __name__ == "__main__":
    game = ArrowsGame()
    game.run()
