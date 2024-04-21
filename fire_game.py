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

        # Scale images to the window width and height
        for key in self.arrow_images:
            self.arrow_images[key] = pygame.transform.scale(self.arrow_images[key], (self.WIDTH, self.HEIGHT))

        # The length of arrow combination (initially equals 2)
        self.count = 2

        # flags
        # flag for game loop
        self.running = True
        # flag if game completed
        self.solved = False
        # flag if intro shown
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
        # Displaying image (assuming self.arrow_images is a dictionary containing images)
        self.screen.blit(self.arrow_images['standard_dark'], (0, 0))

        # Setting the font for the message
        font = pygame.font.SysFont('Papyrus', 36)

        # Creating the message text and text surface
        text = font.render(message, True, (0, 0, 0))

        # Getting the rectangle that surrounds the text to center it on the screen
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Enlarging the rectangle to add padding for the background color
        background_rect = text_rect.inflate(80, 40)

        #Fill the rectangle with color 
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
        # Displaying the standard arrow image
        self.screen.blit(self.arrow_images['standard'], (0, 0))
        pygame.display.update()  
        pygame.time.delay(1000)

        # Iterating over each arrow in the combination
        for arrow in combination:
            # Playing the fire sound effect
            pygame.mixer.Sound('sources/sounds/fire/fire_sound.mp3').play()

            # Displaying the current arrow image
            self.screen.blit(self.arrow_images[arrow], (0, 0))
            pygame.display.update()  
            pygame.time.delay(1000) 

            # Displaying the standard arrow image again
            self.screen.blit(self.arrow_images['standard'], (0, 0))
            pygame.display.update()  

            # Delaying for a short time before displaying the next arrow
            pygame.time.delay(500)  
    
    def show_intro(self):
        """
        Display the game introduction.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            # Play the intro sound
            intro_sound = pygame.mixer.Sound('sources/sounds/fire/dragon_dance_intro.mp3').play(-1)
            
            # Load, scale and display the intro image
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/fire/fire_intro.png"), (600, 600))
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()

            # Wait for the user to press the Enter key to continue
            intro_done = False
            while not intro_done:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        intro_done = True
                pygame.time.Clock().tick(30)

            # Stop playing the intro sound
            intro_sound.stop()
            # Mark the intro as shown
            self.intro_shown = True

    def run(self):
        """
        Run the main game loop.

        Returns:
            bool: True if the game is solved, False otherwise.
        """
        # Show the game introduction
        self.show_intro()
         # Load and play the background music
        pygame.mixer.music.load('sources/sounds/fire/dragon_dance_v2.mp3')
        pygame.mixer.music.play(-1)
        # Main game loop
        while self.running:
            # Display the message (remember the combination)
            self._display_message("Remember the combination")
            # Arrow's combination generation
            combination = self._generate_combination()  
            # Display of arrow combination
            self._display_combination(combination) 

            # Initialize variables for user input
            input_complete = False
            user_input = []

            # Display the message (Your turn) and show standard image
            self._display_message("Your turn")
            pygame.time.delay(200)  
            self.screen.blit(self.arrow_images['standard'], (0, 0))
            pygame.display.update()

            # User input loop
            while not input_complete:
                # Variable to store the direction of the pressed arrow
                arrow = ''
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # Check which arrow key was pressed and append the corresponding direction to user_input
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
                        # Handle window close event
                        pygame.mixer.music.stop()
                        self.running = False
                        return self.solved
                # If an arrow was pressed, play the fire sound effect and display the pressed arrow
                if arrow:
                    pygame.mixer.Sound('sources/sounds/fire/fire_sound.mp3').play()
                    self.screen.blit(self.arrow_images[arrow], (0,0))
                    pygame.display.update()
                    pygame.time.delay(500) 
                    self.screen.blit(self.arrow_images['standard'], (0, 0))
                    pygame.display.update()  
            
            # Check if the user input matches the combination
            if user_input == combination:
                # If the game is completed, display a victory message and end the game
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
                    # If the input is correct but the game is not completed, display a success message
                    self._display_message("Right. Go on...")
                    self.count += 1
            else:
                # If the input is incorrect, display a failure message and end the game
                pygame.mixer.music.stop()
                pygame.mixer.Sound('sources/sounds/fire/dragon_dance_loose.mp3').play()
                self._display_message("Wrong, you haven't mastered fire.")
                pygame.time.delay(3000)
                pygame.mixer.music.stop()
                self.running = False
                return self.solved
                    
# Check if the script is being run as the main program
if __name__ == "__main__":
    game = FireGame()
    game.run()
