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
        
        self.font = pygame.font.Font(None, 36)
        self.options = ["Air", "Water", "Earth", "Fire"]
        self.selected_option = 0
        self.running = True

        self.completed = False
        
        # Flags to track the state of each game
        self.intro_shown = False
        self.earth_completed = False
        self.fire_completed = False
        self.water_completed = False
        self.air_completed = False
        self.end_shown = False

        self.music_pos = 0 
        

        # Load element animation images and scale them to 300x300
        self.animations = {
            "Air": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/air{}.jpeg".format(i)), (300, 300)) for i in [1, 2, 3, 2]],
            "Water": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/water{}.jpeg".format(i)), (300, 300)) for i in [1, 2, 3, 2]],
            "Earth": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/earth{}.jpeg".format(i)), (300, 300)) for i in [1, 2, 3, 2]],
            "Fire": [pygame.transform.scale(pygame.image.load("sources/images/main_menu/fire{}.jpeg".format(i)), (300, 300)) for i in [1, 2, 3, 2]]
        }

        self.stable_icons = {
            "Air": pygame.transform.scale(pygame.image.load("sources/images/main_menu/air_dark.jpeg"), (300, 300)),
            "Water": pygame.transform.scale(pygame.image.load("sources/images/main_menu/water_dark.jpeg"), (300, 300)),
            "Earth": pygame.transform.scale(pygame.image.load("sources/images/main_menu/earth_dark.jpeg"), (300, 300)),
            "Fire": pygame.transform.scale(pygame.image.load("sources/images/main_menu/fire_dark.jpeg"), (300, 300))
        }

    def draw_menu(self):
        """
        Draw the main menu with animated options.
        """
        self.screen.fill(self.GREY)
        num_rows = 2
        num_cols = 2
        tile_width = self.WIDTH // num_cols
        tile_height = self.HEIGHT // num_rows
        for i in range(num_rows):
            for j in range(num_cols):
                index = i * num_cols + j
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
                    frame_index = pygame.time.get_ticks() // 400 % len(self.animations[option])  # Calculate frame index based on time
                    option_icon = self.animations[option][frame_index]  # Get current frame of animation
                
                # Blit the icon to the screen
                icon_rect = option_icon.get_rect(center=((j + 0.5) * tile_width, (i + 0.5) * tile_height))
                self.screen.blit(option_icon, icon_rect)
                
        pygame.display.update()


    def handle_click(self, x, y):
        """
        Handle mouse click events on the main menu options.

        Args:
            x (int): The x-coordinate of the mouse click.
            y (int): The y-coordinate of the mouse click.
        """
        num_rows = 2
        num_cols = 2
        tile_width = self.WIDTH // num_cols
        tile_height = self.HEIGHT // num_rows
        row = y // tile_height
        col = x // tile_width
        index = row * num_cols + col
        if index < len(self.options):
            music_pos = pygame.mixer.music.get_pos()
            selected_option = self.options[index]
            if selected_option == "Air" and not self.air_completed:
                # pygame.mixer.Sound('sources/sounds/main_menu/air.mp3').play()
                # pygame.time.delay(2000)
                pygame.mixer.music.pause()
                air_game = AirGame()
                self.air_completed = air_game.start()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Water" and not self.water_completed:
                # pygame.mixer.Sound('sources/sounds/main_menu/water.mp3').play()
                # pygame.time.delay(2000)
                pygame.mixer.music.pause()
                water_game = WaterGame()
                self.water_completed = water_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Earth" and not self.earth_completed:
                # pygame.mixer.Sound('sources/sounds/main_menu/Earth.mp3').play()
                # pygame.time.delay(2000)
                pygame.mixer.music.pause()
                earth_game = EarthGame()
                self.earth_completed = earth_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            elif selected_option == "Fire" and not self.fire_completed:
                # pygame.mixer.Sound('sources/sounds/main_menu/fire.mp3').play()
                # pygame.time.delay(2000)
                pygame.mixer.music.pause()
                fire_game = FireGame()
                self.fire_completed = fire_game.run()
                pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
                pygame.mixer.music.play(-1, music_pos)
            pygame.display.set_caption("Avatar: The last airbender")

    
    def show_intro(self):
        """
        Display the introduction to the game.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            intro = pygame.mixer.Sound('sources/sounds/main_menu/intro.mp3')
            intro.play()
            intro.set_volume(0.4)
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/main_menu/intro1.jpeg"), (600, 600))
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()
            pygame.time.delay(5000)
            self.intro_shown = True


    def show_ending_poster(self):
        """
        Display the ending poster of the game.
        """
        if not self.end_shown:
            pygame.mixer.music.load('sources/sounds/main_menu/end.mp3')
            pygame.mixer.music.play(-1)
            self.end_shown = True
            ending_image = pygame.transform.scale(pygame.image.load("sources/images/main_menu/end1.jpeg"), (600, 600))
            self.screen.blit(ending_image, (0, 0))
            pygame.display.update()

    def run(self):
        """
        Run the main menu loop.
        """
        # Show intro
        self.show_intro()
        pygame.mixer.music.load('sources/sounds/main_menu/menu.mp3')
        pygame.mixer.music.play(-1) 
        while self.running:
            if not self.completed:
                self.draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        self.handle_click(x, y)
                # If all games are successfully completed, show the ending poster
                if self.air_completed and self.water_completed and self.earth_completed and self.fire_completed:
                    self.completed = True
                    pygame.mixer.music.stop()
            elif self.completed:
                self.show_ending_poster()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
