import pygame
import sys
from air_game import AirGame
from water_game import WaterGame
from earth_game import EarthGame
from fire_game import FireGame

class MainMenu:
    """
    A class representing the main menu of the game, providing options to play different mini-games.
    """
    def __init__(self):
        """
        Initialize the main menu.
        """
        pygame.init()
        pygame.mixer.init()
        
        # Window size
        self.WIDTH, self.HEIGHT = 600, 600
        
        # Colors
        self.GREY = (156, 156, 156)
        self.BLACK = (0, 0, 0)
        
        # Create window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Avatar: The last airbender")
        
        # Menu options
        self.options = ["Air", "Water", "Earth", "Fire"]
        # Index of the currently selected option
        self.selected_option = 0

        # Define the number of rows and columns for menu options
        self.num_rows = 2
        self.num_cols = 2

        # Flag to control the main loop
        self.running = True
        
        # Flags to track the completion state of each game
        self.intro_shown = False
        self.earth_completed = False
        self.fire_completed = False
        self.water_completed = False
        self.air_completed = False
        self.end_shown = False

        # Flag to track if all game completed
        self.completed = False

        # Position of the music playback
        self.music_pos = 0 
        
        # Load element animation images and scale them
        self.animations = {
            "Air": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/air{}.jpeg".format(i)), (self.WIDTH//2, self.HEIGHT//2)) for i in [1, 2, 3, 2]],
            "Water": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/water{}.jpeg".format(i)), (self.WIDTH//2, self.HEIGHT//2)) for i in [1, 2, 3, 2]],
            "Earth": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/earth{}.jpeg".format(i)), (self.WIDTH//2, self.HEIGHT//2)) for i in [1, 2, 3, 2]],
            "Fire": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/fire{}.jpeg".format(i)), (self.WIDTH//2, self.HEIGHT//2)) for i in [1, 2, 3, 2]]
        }

         # Load stable icons for each element and scale them
        self.stable_icons = {
            "Air": pygame.transform.scale(pygame.image.load("sources/images/main_menu/air_dark.jpeg"), (self.WIDTH//2, self.HEIGHT//2)),
            "Water": pygame.transform.scale(pygame.image.load("sources/images/main_menu/water_dark.jpeg"), (self.WIDTH//2, self.HEIGHT//2)),
            "Earth": pygame.transform.scale(pygame.image.load("sources/images/main_menu/earth_dark.jpeg"), (self.WIDTH//2, self.HEIGHT//2)),
            "Fire": pygame.transform.scale(pygame.image.load("sources/images/main_menu/fire_dark.jpeg"), (self.WIDTH//2, self.HEIGHT//2))
        }

    def draw_menu(self):
        """
        Draw the main menu with animated options.
        """
        # Fill the screen with grey color
        self.screen.fill(self.GREY)

        # Calculate the width and height of each menu tile
        tile_width = self.WIDTH // self.num_cols
        tile_height = self.HEIGHT // self.num_rows

        # Iterate over the rows and columns to draw each menu option
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                index = i * self.num_cols + j
                option = self.options[index]
                
                # Check if the game is completed and show stable icon instead of animation
                if option == "Air" and self.air_completed:
                    option_icon = self.stable_icons[option]
                elif option == "Water" and self.water_completed:
                    option_icon = self.stable_icons[option]
                elif option == "Earth" and self.earth_completed:
                    option_icon = self.stable_icons[option]
                elif option == "Fire" and self.fire_completed:
                    option_icon = self.stable_icons[option]
                else:
                    # Calculate the frame index for animation based on time
                    frame_index = pygame.time.get_ticks() // 400 % len(self.animations[option]) 
                    # Get the current frame of animation
                    option_icon = self.animations[option][frame_index] 
                
                # Calculate the position to blit the icon
                icon_rect = option_icon.get_rect(center=((j + 0.5) * tile_width, (i + 0.5) * tile_height))
                # Blit the icon to the screen
                self.screen.blit(option_icon, icon_rect)
        mouse_pos = pygame.mouse.get_pos()
        img_of_cursor = pygame.transform.scale(pygame.image.load("sources/images/main_menu/mouse_cursor.png").convert_alpha(),(30,40))
        self.screen.blit(img_of_cursor, mouse_pos)        
        pygame.display.update()


    def handle_click(self, x, y):
        """
        Handle mouse click events on the main menu options.

        Args:
            x (int): The x-coordinate of the mouse click.
            y (int): The y-coordinate of the mouse click.
        """
        # Calculate the width and height of each menu tile
        tile_width = self.WIDTH // self.num_cols
        tile_height = self.HEIGHT // self.num_rows

         # Calculate the row and column of the clicked tile
        row = y // tile_height
        col = x // tile_width

        # Calculate the index of the clicked option
        index = row * self.num_cols + col

        # Check if the clicked index is within the range of options
        if index < len(self.options):
            # Get the current position of music playback
            music_pos = pygame.mixer.music.get_pos()
            # Get the selected option
            selected_option = self.options[index]

            # Play corresponding game if not already completed
            if selected_option == "Air" and not self.air_completed:
                pygame.mixer.Sound('sources/sounds/main_menu/air.mp3').play()
                pygame.mixer.music.pause()
                air_game = AirGame()
                self.air_completed = air_game.start()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Water" and not self.water_completed:
                pygame.mixer.Sound('sources/sounds/main_menu/water.mp3').play()
                pygame.mixer.music.pause()
                water_game = WaterGame()
                self.water_completed = water_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Earth" and not self.earth_completed:
                pygame.mixer.Sound('sources/sounds/main_menu/earth.mp3').play()
                pygame.mixer.music.pause()
                earth_game = EarthGame()
                self.earth_completed = earth_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Fire" and not self.fire_completed:
                pygame.mixer.Sound('sources/sounds/main_menu/fire.mp3').play()
                pygame.mixer.music.pause()
                fire_game = FireGame()
                self.fire_completed = fire_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)

            pygame.display.set_caption("Avatar: The last airbender")

    
    def show_intro(self):
        """
        Display the intro to the main game.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            # Load and play the intro sound
            intro = pygame.mixer.Sound('sources/sounds/main_menu/intro.mp3')
            intro.play()

            # Set volume
            intro.set_volume(0.4)

            # Load and display the intro image
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/main_menu/intro1.jpeg"), (600, 600))
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()

            # Delay for 5 seconds to allow intro to play
            pygame.time.delay(5000)
            # Mark the intro as shown
            self.intro_shown = True


    def show_ending_poster(self):
        """
        Display the ending poster of the game.
        """
        # Display the ending poster only if it has not been displayed yet
        if not self.end_shown:
            # Load and play the ending music
            pygame.mixer.music.load('sources/sounds/main_menu/end.mp3')
            pygame.mixer.music.play(-1)

            # Load and display the ending image and mark the end poster as shown
            self.end_shown = True
            ending_image = pygame.transform.scale(pygame.image.load("sources/images/main_menu/end1.jpeg"), (600, 600))
            self.screen.blit(ending_image, (0, 0))
            pygame.display.update()

    def run(self):
        """
        Run the main menu loop.
        """
        # Show the introduction
        pygame.mouse.set_visible(False)
        self.show_intro()

        # Load and play the menu music
        pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
        pygame.mixer.music.play(-1) 

        while self.running:
            # Check that not all game are completed
            if not self.completed:
                # Draw the main menu
                self.draw_menu()
                # Handle mouse click events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        self.handle_click(x, y)
                # Check if all games are completed to show the ending poster
                if self.air_completed and self.water_completed and self.earth_completed and self.fire_completed:
                    self.completed = True
                    pygame.mixer.music.stop()
            # If all games completed show ending poster
            elif self.completed:
                self.show_ending_poster()
                # Check for quit event to exit the loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

# Check if the script is being run as the main program
if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
