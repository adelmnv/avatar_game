import pygame
import sys
import os
import random

class FireGame:
    """
    A class representing the 'Fire - The Dancing Dragon' game.
    """

    def __init__(self):
        """
        Initialize the game.
        """
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

        self.running = True

        self.count = 2

        self.solved = False

        self.intro_shown = False

    def _generate_combination(self):
        """
        Generate a random combination of arrows.

        Returns:
            list: A list containing the arrow directions in the generated combination.
        """
        arrows = ['up', 'down', 'left', 'right']
        return [random.choice(arrows) for _ in range(self.count)]

    def _display_message(self, message):
        """
        Display a message on the screen.

        Args:
            message (str): The message to be displayed.
        """
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
        """
        Display the arrow combination on the screen.

        Args:
            combination (list): A list containing the arrow directions to be displayed.
        """
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
    
    def show_intro(self):
        """
        Display the game introduction.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            intro_sound = pygame.mixer.Sound('sources/sounds/fire/dragon_dance_intro.mp3').play(-1)
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/fire/fire_intro.png"), (600, 600))
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()
            intro_done = False
            while not intro_done:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        intro_done = True
                pygame.time.Clock().tick(30)
            
            intro_sound.stop()
            self.intro_shown = True

    def run(self):
        """
        Run the main game loop.

        Returns:
            bool: True if the game is solved, False otherwise.
        """
        self.show_intro()
        pygame.mixer.music.load('sources/sounds/fire/dragon_dance_v2.mp3')
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
                        pygame.mixer.music.stop()
                        self.running = False
                        return self.solved
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
                    self.solved = True
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound('sources/sounds/fire/dragon_dance_win.mp3').play()
                    self._display_message("You've managed to master fire!")
                    pygame.time.delay(3000)
                    pygame.mixer.music.stop()
                    self.running = False
                    return self.solved
                else:
                    self._display_message("Right. Go on...")
                    self.count += 1
            else:
                pygame.mixer.music.stop()
                pygame.mixer.Sound('sources/sounds/fire/dragon_dance_loose.mp3').play()
                self._display_message("Wrong, you haven't mastered fire.")
                pygame.time.delay(3000)
                pygame.mixer.music.stop()
                self.running = False
                return self.solved
                    



if __name__ == "__main__":
    game = ArrowsGame()
    game.run()
